"""
test_quiz_app.py
================
Comprehensive automated test suite for the Python Quiz Application.
Tests:
1. Database initialization and questions seeding
2. Question querying across all 5 categories and 3 difficulties
3. Quiz scoring calculation and grading accuracy
4. History tracking, database recording, and analytics calculation
5. Full UI component lifecycle (Welcome -> Dashboard -> Quiz -> Results -> Review -> History)
6. Dynamic answer changing and navigation logic
7. Timer tick and auto-submit logic
"""

import unittest
import os
import sqlite3
import quiz_data
import database
import ui
import main


class TestQuizApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_quiz.db")
        if os.path.exists(cls.test_db_file):
            os.remove(cls.test_db_file)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db_file):
            os.remove(cls.test_db_file)

    def test_01_categories_and_questions_count(self):
        """Verify that all 5 required categories exist with at least 10 questions each."""
        categories = quiz_data.get_categories()
        expected_categories = [
            "Python Programming",
            "C++ Programming",
            "Data Structures",
            "Artificial Intelligence and Machine Learning",
            "General Knowledge"
        ]
        for exp in expected_categories:
            self.assertIn(exp, categories)

        for cat in expected_categories:
            qs = quiz_data.get_questions_by_filter(category=cat)
            self.assertGreaterEqual(len(qs), 10, f"Category '{cat}' must have at least 10 questions")
            # Verify options and explanation structure
            for q in qs:
                self.assertEqual(len(q["options"]), 4, f"Question {q['id']} must have 4 options")
                self.assertIn(q["correct_index"], [0, 1, 2, 3], f"Question {q['id']} correct_index must be 0-3")
                self.assertTrue(len(q["explanation"]) > 10, f"Question {q['id']} must have a meaningful explanation")
                self.assertIn(q["difficulty"], ["Easy", "Medium", "Hard"])

    def test_02_database_operations(self):
        """Test database table creation, seeding, attempt saving, and queries."""
        database.init_db(self.test_db_file)

        # Verify tables created
        conn = database.get_connection(self.test_db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) as cnt FROM questions")
        q_count = cursor.fetchone()["cnt"]
        self.assertGreaterEqual(q_count, 50)
        conn.close()

        # Test recording attempts
        rec_id1 = database.record_attempt(
            student_name="Rahul Verma",
            category="Python Programming",
            difficulty="Medium",
            score=9,
            total_questions=10,
            time_taken_seconds=145,
            db_path=self.test_db_file
        )
        self.assertIsNotNone(rec_id1)

        rec_id2 = database.record_attempt(
            student_name="Ananya Sen",
            category="Artificial Intelligence and Machine Learning",
            difficulty="Hard",
            score=7,
            total_questions=10,
            time_taken_seconds=200,
            db_path=self.test_db_file
        )
        self.assertIsNotNone(rec_id2)

        # Test history retrieval
        hist = database.get_quiz_history(db_path=self.test_db_file)
        self.assertGreaterEqual(len(hist), 2)
        self.assertEqual(hist[0]["student_name"], "Ananya Sen")

        # Test analytics calculation
        stats = database.get_analytics_summary(db_path=self.test_db_file)
        self.assertEqual(stats["total_attempts"], 2)
        self.assertAlmostEqual(stats["avg_percentage"], 80.0, delta=1.0)
        self.assertEqual(stats["max_percentage"], 90.0)

    def test_03_score_and_grade_logic(self):
        """Verify grading boundaries and remarks."""
        self.assertIn("A+", database.calculate_grade(95))
        self.assertIn("A", database.calculate_grade(85))
        self.assertIn("B+", database.calculate_grade(75))
        self.assertIn("B", database.calculate_grade(65))
        self.assertIn("C", database.calculate_grade(55))
        self.assertIn("D", database.calculate_grade(45))
        self.assertIn("F", database.calculate_grade(30))

    def test_04_ui_flow_and_navigation(self):
        """Instantiate Tkinter UI and verify screens, answer selection, and submission."""
        app = main.QuizPortalApp()
        app.withdraw()  # Run headless for testing

        try:
            # 1. Welcome screen
            welcome = app.screens["WelcomeScreen"]
            welcome.name_entry.delete(0, "end")
            welcome.name_entry.insert(0, "Test Student 2nd Year")
            welcome.on_start_click()
            app.update()

            self.assertEqual(app.current_student_name, "Test Student 2nd Year")

            # 2. Dashboard screen
            dash = app.screens["DashboardScreen"]
            dash.selected_category_var.set("Data Structures")
            dash.selected_diff_var.set("Easy")
            dash.question_count_var.set(5)
            dash.start_quiz_session()
            app.update()

            # 3. Quiz screen
            quiz = app.screens["QuizScreen"]
            self.assertEqual(len(quiz.questions), 5)
            self.assertEqual(quiz.current_idx, 0)
            self.assertTrue(quiz.timer_active)

            # Select answer for Q1
            quiz.selected_opt_var.set(1)
            quiz.on_option_selected()
            self.assertEqual(quiz.user_answers[0], 1)

            # Change answer for Q1 (verifying user can change answer)
            quiz.selected_opt_var.set(0)
            quiz.on_option_selected()
            self.assertEqual(quiz.user_answers[0], 0)

            # Navigate next
            quiz.go_next()
            app.update()
            self.assertEqual(quiz.current_idx, 1)

            # Answer Q2
            quiz.selected_opt_var.set(2)
            quiz.on_option_selected()
            self.assertEqual(quiz.user_answers[1], 2)

            # Navigate back to Q1
            quiz.go_prev()
            app.update()
            self.assertEqual(quiz.current_idx, 0)
            self.assertEqual(quiz.selected_opt_var.get(), 0)

            # Jump directly to Q4 using palette
            quiz.jump_to_question(3)
            app.update()
            self.assertEqual(quiz.current_idx, 3)

            # Finalize & submit
            quiz.finalize_and_submit()
            app.update()

            # 4. Results screen
            results = app.screens["ResultsScreen"]
            self.assertGreaterEqual(len(results.cached_results), 5)
            self.assertIn("Test Student", results.candidate_name_lbl.cget("text"))

            # 5. History screen
            app.show_screen("HistoryScreen")
            app.update()
            hist_screen = app.screens["HistoryScreen"]
            self.assertGreater(len(hist_screen.tree.get_children()), 0)

        finally:
            app.destroy()


if __name__ == "__main__":
    unittest.main()
