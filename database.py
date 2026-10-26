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
from quiz_data import QUESTIONS_DATA

DEFAULT_DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz_portal.db")


def get_connection(db_path=None):
    """Create and return a database connection with row factory enabled."""
    path = db_path or DEFAULT_DB_FILE
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    """
    Initializes tables for questions and quiz attempts.
    Seeds the questions table if currently empty.
    """
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

    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_attempts
        (student_name, category, difficulty, score, total_questions, percentage, grade, time_taken_seconds, attempt_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, category, difficulty, sc, total, percentage, grade, time_taken, timestamp))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def fetch_questions(category="All", difficulty="All", limit=10, randomize=True, db_path=None):
    """
    Queries questions from SQLite database matching category and difficulty.
    Returns list of question dictionaries formatted for the UI.
    """
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


def get_quiz_history(limit=100, category_filter=None, student_filter=None, db_path=None):
    """Retrieves previous quiz attempts from SQLite database."""
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


def get_analytics_summary(db_path=None):
    """Calculates overall statistics across all quiz attempts."""
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


def clear_all_history(db_path=None):
    """Deletes all records from the quiz_attempts table."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quiz_attempts")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='quiz_attempts'")
    conn.commit()
    conn.close()
