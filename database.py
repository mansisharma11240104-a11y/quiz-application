"""
database.py
===========
SQLite Database Manager for the Python Quiz Application.
Handles initialization, questions persistence/seeding, attempt history tracking,
scoring metrics, and analytics queries.
"""

import sqlite3
import os
import datetime
import tempfile
from quiz_data import QUESTIONS_DATA

DEFAULT_DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz_portal.db")


def get_db_path(db_path=None):
    """
    Returns the appropriate database path.
    On serverless platforms like Vercel or AWS Lambda, the deployment directory is
    strictly read-only, so the database is placed in the writable temporary directory.
    """
    if db_path:
        return db_path

    # Check for Vercel, AWS Lambda, or other serverless/read-only container markers
    is_serverless = bool(
        os.environ.get("VERCEL") or 
        os.environ.get("AWS_LAMBDA_FUNCTION_NAME") or 
        os.environ.get("NOW_REGION")
    )

    if is_serverless:
        target_dir = tempfile.gettempdir()
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Verify if the current directory is writable
        test_file = os.path.join(current_dir, f".write_test_{os.getpid()}")
        try:
            with open(test_file, "w") as f:
                f.write("1")
            os.remove(test_file)
            target_dir = current_dir
        except Exception:
            target_dir = tempfile.gettempdir()

    target_db = os.path.join(target_dir, "quiz_portal.db")

    # If target is in temp and doesn't exist yet, copy the pre-seeded bundled database
    bundled_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz_portal.db")
    if target_db != bundled_db and os.path.exists(bundled_db) and not os.path.exists(target_db):
        try:
            import shutil
            shutil.copyfile(bundled_db, target_db)
        except Exception as e:
            print(f"Notice: Failed to copy bundled db to {target_db}: {e}")

    return target_db


def get_connection(db_path=None):
    """Create and return a database connection with row factory enabled."""
    path = get_db_path(db_path)
    try:
        conn = sqlite3.connect(path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Warning: sqlite3.connect failed for {path}: {e}. Using in-memory fallback.")
        conn = sqlite3.connect(":memory:", timeout=10)
        conn.row_factory = sqlite3.Row
        return conn


def init_db(db_path=None):
    """
    Initializes tables for questions and quiz attempts.
    Seeds the questions table if currently empty.
    """
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        # 1. Questions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                category TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_index INTEGER NOT NULL,
                explanation TEXT NOT NULL
            )
        """)

        # 2. Quiz Attempts Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                category TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percentage REAL NOT NULL,
                grade TEXT NOT NULL,
                time_taken_seconds INTEGER NOT NULL,
                attempt_timestamp TEXT NOT NULL
            )
        """)

        conn.commit()

        # Check if questions need to be seeded
        cursor.execute("SELECT COUNT(*) AS cnt FROM questions")
        count = cursor.fetchone()["cnt"]

        if count == 0:
            seed_questions(QUESTIONS_DATA, conn)

        conn.close()
    except Exception as e:
        print(f"init_db notice: {e}")


def seed_questions(questions_list, conn=None):
    """Seed initial questions into the database."""
    should_close = False
    if conn is None:
        conn = get_connection()
        should_close = True

    cursor = conn.cursor()
    for q in questions_list:
        cursor.execute("""
            INSERT OR REPLACE INTO questions 
            (id, category, difficulty, question, option_a, option_b, option_c, option_d, correct_index, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            q["id"],
            q["category"],
            q["difficulty"],
            q["question"],
            q["options"][0],
            q["options"][1],
            q["options"][2],
            q["options"][3],
            q["correct_index"],
            q["explanation"]
        ))

    conn.commit()
    if should_close:
        conn.close()


def calculate_grade(percentage):
    """Calculate academic grade and remarks based on percentage."""
    if percentage >= 90.0:
        return "A+ (Outstanding)"
    elif percentage >= 80.0:
        return "A (Excellent)"
    elif percentage >= 70.0:
        return "B+ (Very Good)"
    elif percentage >= 60.0:
        return "B (Good)"
    elif percentage >= 50.0:
        return "C (Satisfactory)"
    elif percentage >= 40.0:
        return "D (Pass)"
    else:
        return "F (Needs Improvement)"


def record_attempt(student_name, category, difficulty, score, total_questions, time_taken_seconds, db_path=None):
    """
    Saves a completed quiz attempt into SQLite and returns the record ID.
    Validates input parameters to prevent invalid state.
    """
    name = (student_name or "").strip() or "Guest Student"
    total = max(1, int(total_questions))
    sc = max(0, min(int(score), total))
    percentage = round((sc / total) * 100, 2)
    grade = calculate_grade(percentage)
    time_taken = max(0, int(time_taken_seconds))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fallback_id = int(datetime.datetime.now().strftime("%y%m%d%H%M%S"))
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO quiz_attempts
            (student_name, category, difficulty, score, total_questions, percentage, grade, time_taken_seconds, attempt_timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, category, difficulty, sc, total, percentage, grade, time_taken, timestamp))
        conn.commit()
        new_id = cursor.lastrowid or fallback_id
        conn.close()
        return new_id
    except Exception as e:
        print(f"record_attempt warning: {e}")
        return fallback_id


def fetch_questions(category="All", difficulty="All", limit=10, randomize=True, db_path=None):
    """
    Queries questions from SQLite database matching category and difficulty.
    Falls back gracefully to in-memory question bank if database read fails.
    """
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM questions WHERE 1=1"
        params = []

        if category and category != "All":
            query += " AND category = ?"
            params.append(category)

        if difficulty and difficulty != "All":
            query += " AND difficulty = ?"
            params.append(difficulty)

        if randomize:
            query += " ORDER BY RANDOM()"
        else:
            query += " ORDER BY id ASC"

        if limit and limit > 0:
            query += " LIMIT ?"
            params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        if rows:
            questions = []
            for r in rows:
                questions.append({
                    "id": r["id"],
                    "category": r["category"],
                    "difficulty": r["difficulty"],
                    "question": r["question"],
                    "options": [r["option_a"], r["option_b"], r["option_c"], r["option_d"]],
                    "correct_index": r["correct_index"],
                    "explanation": r["explanation"]
                })
            return questions
    except Exception as e:
        print(f"fetch_questions SQLite warning: {e}")

    # Fallback to quiz_data in-memory
    import random
    from quiz_data import get_questions_by_filter
    qs = get_questions_by_filter(category=category, difficulty=difficulty)
    if randomize:
        qs = list(qs)
        random.shuffle(qs)
    return qs[:limit] if limit else qs


def get_quiz_history(limit=100, category_filter=None, student_filter=None, db_path=None):
    """Retrieves previous quiz attempts from SQLite database."""
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM quiz_attempts WHERE 1=1"
        params = []

        if category_filter and category_filter != "All":
            query += " AND category = ?"
            params.append(category_filter)

        if student_filter and student_filter.strip():
            query += " AND student_name LIKE ?"
            params.append(f"%{student_filter.strip()}%")

        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        history = []
        for r in rows:
            history.append({
                "id": r["id"],
                "student_name": r["student_name"],
                "category": r["category"],
                "difficulty": r["difficulty"],
                "score": r["score"],
                "total_questions": r["total_questions"],
                "percentage": r["percentage"],
                "grade": r["grade"],
                "time_taken_seconds": r["time_taken_seconds"],
                "timestamp": r["attempt_timestamp"]
            })
        return history
    except Exception as e:
        print(f"get_quiz_history warning: {e}")
        return []


def get_analytics_summary(db_path=None):
    """Calculates overall statistics across all quiz attempts."""
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                COUNT(*) AS total_attempts,
                COALESCE(AVG(percentage), 0) AS avg_percentage,
                COALESCE(MAX(percentage), 0) AS max_percentage,
                COALESCE(MIN(percentage), 0) AS min_percentage
            FROM quiz_attempts
        """)
        overview = cursor.fetchone()

        cursor.execute("""
            SELECT category, COUNT(*) as cnt 
            FROM quiz_attempts 
            GROUP BY category 
            ORDER BY cnt DESC 
            LIMIT 1
        """)
        top_cat_row = cursor.fetchone()
        most_popular_category = top_cat_row["category"] if top_cat_row else "None"

        cursor.execute("""
            SELECT student_name, MAX(percentage) as best_pct
            FROM quiz_attempts
            GROUP BY student_name
            ORDER BY best_pct DESC, id ASC
            LIMIT 1
        """)
        top_scorer_row = cursor.fetchone()
        top_scorer = f"{top_scorer_row['student_name']} ({top_scorer_row['best_pct']}%)" if top_scorer_row else "None"

        conn.close()

        return {
            "total_attempts": overview["total_attempts"],
            "avg_percentage": round(overview["avg_percentage"], 1),
            "max_percentage": round(overview["max_percentage"], 1),
            "most_popular_category": most_popular_category,
            "top_scorer": top_scorer
        }
    except Exception as e:
        print(f"get_analytics_summary warning: {e}")
        return {
            "total_attempts": 0,
            "avg_percentage": 0.0,
            "max_percentage": 0.0,
            "most_popular_category": "None",
            "top_scorer": "None"
        }


def clear_all_history(db_path=None):
    """Deletes all records from the quiz_attempts table."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quiz_attempts")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='quiz_attempts'")
    conn.commit()
    conn.close()
