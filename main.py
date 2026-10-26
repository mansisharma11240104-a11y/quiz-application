"""
main.py
=======
Application entry point for the Python Quiz Application.
Initializes the database, configures the master Tkinter window, registers
theme styles and screen navigation, and starts the main event loop.

B.Tech 2nd-Year CSE AIML College Project.
"""

import sys
import tkinter as tk
from tkinter import messagebox
import database
import ui


class QuizPortalApp(tk.Tk):
    """Master Application Window and Screen Router."""
    def __init__(self):
        super().__init__()

        # Window Metadata & Geometry
        self.title("BrainQuest — Technical Quiz & Assessment Portal (B.Tech CSE AIML)")
        self.minsize(960, 680)
        self.geometry("1020x720")
        self.configure(bg=ui.THEME["bg_main"])

        # Center window on screen
        self.center_window(1020, 720)

        # Application Global State
        self.current_student_name = "Student"
        self.active_quiz_data = None

        # Initialize SQLite database
        database.init_db()

        # Apply Modern TTK Styles
        ui.apply_custom_styles(self)

        # Screen Container (Stack)
        self.container = tk.Frame(self, bg=ui.THEME["bg_main"])
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Screen Registry
        self.screens = {}
        for ScreenClass in (
            ui.WelcomeScreen,
            ui.DashboardScreen,
            ui.QuizScreen,
            ui.ResultsScreen,
            ui.HistoryScreen
        ):
            screen_name = ScreenClass.__name__
            screen_instance = ScreenClass(parent=self.container, controller=self)
            self.screens[screen_name] = screen_instance
            screen_instance.grid(row=0, column=0, sticky="nsew")

        # Intercept window close to clean up timers
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Show initial welcome screen
        self.show_screen("WelcomeScreen")

    def center_window(self, width, height):
        """Calculates center screen coordinates and sets window geometry."""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_screen(self, screen_name):
        """Brings the requested screen to the front and triggers any setup hooks."""
        screen = self.screens.get(screen_name)
        if screen:
            # Lifecycle hooks
            if screen_name == "DashboardScreen":
                screen.update_greeting()
            elif screen_name == "HistoryScreen":
                screen.load_history_records()

            screen.tkraise()

    def init_quiz(self, category, difficulty, questions):
        """Passes selected quiz configuration to QuizScreen."""
        quiz_screen = self.screens["QuizScreen"]
        quiz_screen.setup_quiz_data(category, difficulty, questions)

    def display_quiz_results(self, attempt_id, category, difficulty, score, total, time_spent_seconds, detailed_results):
        """Passes completed quiz score and answer breakdown to ResultsScreen."""
        results_screen = self.screens["ResultsScreen"]
        results_screen.populate_results(
            attempt_id=attempt_id,
            category=category,
            difficulty=difficulty,
            score=score,
            total=total,
            time_spent_seconds=time_spent_seconds,
            detailed_results=detailed_results
        )

    def on_exit(self):
        """Handles application shutdown gracefully."""
        quiz_screen = self.screens.get("QuizScreen")
        if quiz_screen and getattr(quiz_screen, "timer_active", False):
            confirm = messagebox.askyesno(
                "Quit Quiz?",
                "A quiz session is currently running! Are you sure you want to abandon it and exit?"
            )
            if not confirm:
                return
            quiz_screen.stop_countdown_timer()

        self.destroy()


def main():
    """Application main entry point."""
    try:
        app = QuizPortalApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"An unexpected error occurred:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
