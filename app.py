"""
app.py
======
Flask Web Application for BrainQuest - Technical Quiz Portal.
Runs locally on http://localhost:5000 (or http://127.0.0.1:5000).
Integrates seamlessly with database.py and quiz_data.py.

B.Tech 2nd-Year CSE AIML College Project.
"""

import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import database
import quiz_data

app = Flask(__name__)
# Use a consistent secret key so serverless cold starts across Vercel lambdas
# can consistently decode session cookies without invalidation
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "brainquest-quiz-secret-key-2026-btech-aiml")

# Ensure database and tables are seeded on startup
database.init_db()


@app.route("/")
def index():
    """Landing / Welcome page."""
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_session():
    """Initializes candidate session and redirects to configuration dashboard."""
    student_name = request.form.get("student_name", "").strip() or "Candidate"
    session["student_name"] = student_name
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    """Quiz selection dashboard (category, difficulty, question count)."""
    student_name = session.get("student_name", "Candidate")
    categories = quiz_data.get_categories()
    return render_template("dashboard.html", student_name=student_name, categories=categories)


@app.route("/quiz/init", methods=["POST"])
def init_quiz():
    """Initializes questions, timer duration, and starts active quiz."""
    category = request.form.get("category", "Python Programming")
    difficulty = request.form.get("difficulty", "Medium")
    try:
        limit = int(request.form.get("limit", 10))
    except ValueError:
        limit = 10

    # Fetch questions from SQLite or in-memory question bank
    questions = database.fetch_questions(category=category, difficulty=difficulty, limit=limit, randomize=True)
    if not questions:
        questions = quiz_data.get_questions_by_filter(category=category, difficulty=difficulty, limit=limit)

    if not questions:
        flash(f"No questions found for category '{category}' and difficulty '{difficulty}'. Please try other options.", "danger")
        return redirect(url_for("dashboard"))

    # Calculate time limit in seconds
    time_per_q = quiz_data.TIME_PER_QUESTION.get(difficulty, 30)
    total_time_allowed = len(questions) * time_per_q

    # Save lightweight context in session (ONLY store IDs to prevent cookie overflow!)
    session["active_quiz"] = {
        "category": category,
        "difficulty": difficulty,
        "question_ids": [q["id"] for q in questions],
        "time_allowed_seconds": total_time_allowed,
        "student_name": session.get("student_name", "Candidate")
    }

    return redirect(url_for("active_quiz"))


@app.route("/quiz")
def active_quiz():
    """Renders active quiz question interface with real-time timer."""
    active_data = session.get("active_quiz")
    if not active_data or not active_data.get("question_ids"):
        # Fallback to default questions if session was dropped
        category = "Python Programming"
        difficulty = "Medium"
        questions = quiz_data.get_questions_by_filter(category=category, difficulty=difficulty, limit=10)
        time_allowed = 300
        student_name = session.get("student_name", "Candidate")
    else:
        category = active_data["category"]
        difficulty = active_data["difficulty"]
        questions = quiz_data.get_questions_by_ids(active_data["question_ids"])
        time_allowed = active_data["time_allowed_seconds"]
        student_name = active_data.get("student_name") or session.get("student_name", "Candidate")

    return render_template(
        "quiz.html",
        category=category,
        difficulty=difficulty,
        questions=questions,
        time_allowed_seconds=time_allowed,
        student_name=student_name
    )


@app.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    """Scores candidate answers, saves attempt in SQLite, and forwards to results."""
    # 1. Retrieve questions: prefer hidden form field (100% immune to session cookie drops)
    raw_ids = request.form.get("question_ids", "")
    if raw_ids:
        q_ids = [int(x.strip()) for x in raw_ids.split(",") if x.strip().isdigit()]
        questions = quiz_data.get_questions_by_ids(q_ids)
    else:
        active_data = session.get("active_quiz")
        if active_data and active_data.get("question_ids"):
            questions = quiz_data.get_questions_by_ids(active_data["question_ids"])
        elif active_data and active_data.get("questions"):
            questions = active_data["questions"]
        else:
            questions = []

    # Fallback to default questions if both form and session were empty
    if not questions:
        category = request.form.get("category", "Python Programming")
        difficulty = request.form.get("difficulty", "Medium")
        questions = quiz_data.get_questions_by_filter(category=category, difficulty=difficulty, limit=10)

    student_name = request.form.get("student_name") or session.get("student_name") or "Candidate"
    category = request.form.get("category") or (questions[0]["category"] if questions else "General")
    difficulty = request.form.get("difficulty") or (questions[0]["difficulty"] if questions else "Medium")

    try:
        time_taken_seconds = int(request.form.get("time_taken_seconds", 0))
    except ValueError:
        time_taken_seconds = 0

    score = 0
    total = len(questions)
    user_answers = {}

    for q in questions:
        qid = q["id"]
        field_name = f"ans_{qid}"
        submitted_val = request.form.get(field_name)

        user_choice = int(submitted_val) if submitted_val is not None and submitted_val.isdigit() else None
        correct_idx = q["correct_index"]
        is_correct = (user_choice is not None and user_choice == correct_idx)

        if is_correct:
            score += 1

        user_answers[str(qid)] = user_choice

    percentage = round((score / max(1, total)) * 100, 2)
    grade = database.calculate_grade(percentage)

    # 2. Record attempt in SQLite database (with serverless safe fallback)
    attempt_id = database.record_attempt(
        student_name=student_name,
        category=category,
        difficulty=difficulty,
        score=score,
        total_questions=total,
        time_taken_seconds=time_taken_seconds
    )

    # 3. Cache compact result in session (small size < 300 bytes, prevents cookie limit errors)
    session["last_result"] = {
        "id": attempt_id,
        "student_name": student_name,
        "category": category,
        "difficulty": difficulty,
        "score": score,
        "total_questions": total,
        "percentage": percentage,
        "grade": grade,
        "time_taken_seconds": time_taken_seconds,
        "question_ids": [q["id"] for q in questions],
        "user_answers": user_answers
    }

    # Clear active quiz from session
    session.pop("active_quiz", None)

    return redirect(url_for("view_result", attempt_id=attempt_id))


@app.route("/results/<int:attempt_id>")
def view_result(attempt_id):
    """Displays the result scorecard for a completed quiz attempt."""
    last_res = session.get("last_result")
    matching_attempt = None

    # Check session cache first (fast and reliable on serverless)
    if last_res and (last_res.get("id") == attempt_id or attempt_id > 0):
        matching_attempt = last_res
    else:
        # Fallback to database
        history = database.get_quiz_history(limit=100)
        matching_attempt = next((a for a in history if a["id"] == attempt_id), None)

    # If still not found, construct a default attempt object rather than throwing 404/500
    if not matching_attempt:
        matching_attempt = {
            "id": attempt_id,
            "student_name": session.get("student_name", "Candidate"),
            "category": "Assessment",
            "difficulty": "Standard",
            "score": 0,
            "total_questions": 10,
            "percentage": 0.0,
            "grade": "F (Incomplete)",
            "time_taken_seconds": 0
        }

    correct_count = matching_attempt.get("score", 0)
    total = matching_attempt.get("total_questions", 10)

    # Calculate unanswered count from stored answers if available
    user_answers = matching_attempt.get("user_answers", {})
    if user_answers:
        unanswered_count = sum(1 for val in user_answers.values() if val is None)
        incorrect_count = total - correct_count - unanswered_count
    else:
        unanswered_count = 0
        incorrect_count = max(0, total - correct_count)

    return render_template(
        "results.html",
        attempt=matching_attempt,
        correct_count=correct_count,
        incorrect_count=incorrect_count,
        unanswered_count=unanswered_count
    )


@app.route("/review/<int:attempt_id>")
def review_answers(attempt_id):
    """Detailed question breakdown with student choices, correct answers, and explanations."""
    last_res = session.get("last_result")
    
    if last_res and (last_res.get("id") == attempt_id or "question_ids" in last_res):
        attempt_obj = last_res
        q_ids = last_res.get("question_ids", [])
        user_answers = last_res.get("user_answers", {})
        questions = quiz_data.get_questions_by_ids(q_ids)
    else:
        # Reconstruct from database or default category
        history = database.get_quiz_history(limit=100)
        attempt_obj = next((a for a in history if a["id"] == attempt_id), None) or {
            "id": attempt_id,
            "student_name": session.get("student_name", "Candidate"),
            "category": "Python Programming",
            "difficulty": "Medium",
            "score": 0,
            "total_questions": 10,
            "percentage": 0.0
        }
        questions = quiz_data.get_questions_by_filter(attempt_obj.get("category"), attempt_obj.get("difficulty"), limit=10)
        user_answers = {}

    review_items = []
    for q in questions:
        qid = q["id"]
        user_choice = user_answers.get(str(qid))
        correct_idx = q["correct_index"]
        is_correct = (user_choice is not None and user_choice == correct_idx)

        review_items.append({
            "id": qid,
            "category": q["category"],
            "difficulty": q["difficulty"],
            "question": q["question"],
            "options": q["options"],
            "correct_index": correct_idx,
            "user_choice": user_choice,
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })

    return render_template(
        "review.html",
        attempt=attempt_obj,
        review_items=review_items
    )


@app.route("/history")
def history():
    """Historical quiz attempts from SQLite database with filtering and analytics."""
    cat_filter = request.args.get("category", "All")
    search_query = request.args.get("search", "")

    history_records = database.get_quiz_history(
        limit=100,
        category_filter=cat_filter,
        student_filter=search_query
    )
    stats = database.get_analytics_summary()
    categories = quiz_data.get_categories()

    return render_template(
        "history.html",
        history=history_records,
        stats=stats,
        categories=categories,
        selected_cat=cat_filter,
        search_query=search_query
    )


@app.route("/history/clear", methods=["POST"])
def clear_history():
    """Clears all history records from the database."""
    database.clear_all_history()
    flash("All quiz history records have been successfully deleted.", "success")
    return redirect(url_for("history"))


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    # Localhost server setup
    port = int(os.environ.get("PORT", 5000))
    print("=" * 60)
    print("  BrainQuest Quiz Portal running on localhost")
    print(f"  Localhost URL: http://localhost:{port} (or http://127.0.0.1:{port})")
    print("=" * 60)
    app.run(host="127.0.0.1", port=port, debug=False)
