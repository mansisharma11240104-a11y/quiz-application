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
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(24))

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

    # Fetch questions from SQLite database
    questions = database.fetch_questions(category=category, difficulty=difficulty, limit=limit, randomize=True)
    if not questions:
        flash(f"No questions found for category '{category}' and difficulty '{difficulty}'. Please try other options.", "danger")
        return redirect(url_for("dashboard"))

    # Calculate time limit in seconds
    time_per_q = quiz_data.TIME_PER_QUESTION.get(difficulty, 30)
    total_time_allowed = len(questions) * time_per_q

    # Save active quiz context in session
    session["active_quiz"] = {
        "category": category,
        "difficulty": difficulty,
        "questions": questions,
        "time_allowed_seconds": total_time_allowed
    }

    return redirect(url_for("active_quiz"))


@app.route("/quiz")
def active_quiz():
    """Renders active quiz question interface with real-time timer."""
    active_data = session.get("active_quiz")
    if not active_data or not active_data.get("questions"):
        flash("No active quiz session found. Please select your options and start a new quiz.", "warning")
        return redirect(url_for("dashboard"))

    return render_template(
        "quiz.html",
        category=active_data["category"],
        difficulty=active_data["difficulty"],
        questions=active_data["questions"],
        time_allowed_seconds=active_data["time_allowed_seconds"]
    )


@app.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    """Scores candidate answers, saves attempt in SQLite, and forwards to results."""
    active_data = session.get("active_quiz")
    if not active_data or not active_data.get("questions"):
        flash("Quiz session expired. Please start a new quiz.", "danger")
        return redirect(url_for("dashboard"))

    questions = active_data["questions"]
    student_name = session.get("student_name", "Candidate")
    
    try:
        time_taken_seconds = int(request.form.get("time_taken_seconds", 0))
    except ValueError:
        time_taken_seconds = 0

    score = 0
    total = len(questions)
    review_items = []

    for q in questions:
        qid = q["id"]
        field_name = f"ans_{qid}"
        submitted_val = request.form.get(field_name)

        user_choice = int(submitted_val) if submitted_val is not None and submitted_val.isdigit() else None
        correct_idx = q["correct_index"]
        is_correct = (user_choice is not None and user_choice == correct_idx)

        if is_correct:
            score += 1

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

    # Record attempt in SQLite database
    attempt_id = database.record_attempt(
        student_name=student_name,
        category=active_data["category"],
        difficulty=active_data["difficulty"],
        score=score,
        total_questions=total,
        time_taken_seconds=time_taken_seconds
    )

    # Cache review items in session for instant review
    session["last_review"] = {
        "attempt_id": attempt_id,
        "items": review_items
    }

    # Clear active quiz from session
    session.pop("active_quiz", None)

    return redirect(url_for("view_result", attempt_id=attempt_id))


@app.route("/results/<int:attempt_id>")
def view_result(attempt_id):
    """Displays the result scorecard for a completed quiz attempt."""
    history = database.get_quiz_history(limit=100)
    matching_attempt = next((a for a in history if a["id"] == attempt_id), None)

    if not matching_attempt:
        flash("Attempt record not found.", "danger")
        return redirect(url_for("history"))

    # Calculate metrics
    correct_count = matching_attempt["score"]
    total = matching_attempt["total_questions"]
    
    # Try retrieving from session review cache if available
    last_review = session.get("last_review")
    if last_review and last_review.get("attempt_id") == attempt_id:
        unanswered_count = sum(1 for item in last_review["items"] if item["user_choice"] is None)
        incorrect_count = total - correct_count - unanswered_count
    else:
        unanswered_count = 0
        incorrect_count = total - correct_count

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
    history = database.get_quiz_history(limit=100)
    matching_attempt = next((a for a in history if a["id"] == attempt_id), None)

    if not matching_attempt:
        flash("Attempt record not found.", "danger")
        return redirect(url_for("history"))

    last_review = session.get("last_review")
    if last_review and last_review.get("attempt_id") == attempt_id:
        review_items = last_review["items"]
    else:
        # Reconstruct review items from question bank
        review_items = []
        all_questions = database.fetch_questions(limit=500, randomize=False)
        q_map = {q["id"]: q for q in all_questions}
        for q in all_questions[:matching_attempt["total_questions"]]:
            review_items.append({
                "id": q["id"],
                "category": q["category"],
                "difficulty": q["difficulty"],
                "question": q["question"],
                "options": q["options"],
                "correct_index": q["correct_index"],
                "user_choice": None,
                "is_correct": False,
                "explanation": q["explanation"]
            })

    return render_template(
        "review.html",
        attempt=matching_attempt,
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
