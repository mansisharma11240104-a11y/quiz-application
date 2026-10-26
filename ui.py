"""
ui.py
=====
Modern, attractive, and modular Graphical User Interface for the Python Quiz Application.
Built using Python's standard Tkinter and ttk libraries with custom card-based
styling, responsive layouts, countdown timer, and interactive answer review.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import database
import quiz_data

# =============================================================================
# THEME CONFIGURATION AND PALETTE
# =============================================================================
THEME = {
    "bg_main": "#0B1120",        # Deep Navy / Slate
    "bg_card": "#1E293B",        # Card Surface
    "bg_card_alt": "#243247",    # Card Secondary Surface
    "border": "#334155",         # Border Gray
    "border_focus": "#6366F1",   # Focus Border
    "primary": "#4F46E5",        # Indigo 600
    "primary_hover": "#6366F1",  # Indigo 500
    "primary_light": "#EEF2FF",  # Indigo Tint
    "accent_cyan": "#06B6D4",    # Cyan 500
    "success": "#10B981",        # Emerald 500
    "success_bg": "#064E3B",     # Dark Emerald
    "danger": "#EF4444",         # Red 500
    "danger_bg": "#451A1A",      # Dark Red
    "warning": "#F59E0B",        # Amber 500
    "text_white": "#F8FAFC",     # Light 50
    "text_muted": "#94A3B8",     # Slate 400
    "text_dark": "#0F172A",      # Dark Slate
    "font_family": "Segoe UI",
    "font_mono": "Consolas"
}


def apply_custom_styles(root):
    """Applies modern ttk styles across the entire Tkinter application."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # Treeview Styles for History Table
    style.configure(
        "Modern.Treeview",
        background=THEME["bg_card"],
        foreground=THEME["text_white"],
        fieldbackground=THEME["bg_card"],
        font=(THEME["font_family"], 10),
        rowheight=32,
        borderwidth=0
    )
    style.configure(
        "Modern.Treeview.Heading",
        background=THEME["bg_card_alt"],
        foreground=THEME["text_white"],
        font=(THEME["font_family"], 10, "bold"),
        relief="flat"
    )
    style.map("Modern.Treeview", background=[("selected", THEME["primary"])])
    style.map("Modern.Treeview.Heading", background=[("active", THEME["primary"])])

    # Progress bar style
    style.configure(
        "Modern.Horizontal.TProgressbar",
        troughcolor=THEME["bg_card_alt"],
        background=THEME["primary_hover"],
        thickness=8,
        borderwidth=0
    )


# =============================================================================
# HELPER WIDGETS
# =============================================================================
class ModernCard(tk.Frame):
    """Card container with subtle border and dark slate background."""
    def __init__(self, parent, bg=THEME["bg_card"], border_color=THEME["border"], **kwargs):
        super().__init__(parent, bg=border_color, padx=1, pady=1, **kwargs)
        self.inner = tk.Frame(self, bg=bg, padx=16, pady=16)
        self.inner.pack(fill="both", expand=True)


class PillBadge(tk.Label):
    """Pill-shaped badge for categories, difficulties, and status."""
    def __init__(self, parent, text, bg_color=THEME["primary"], fg_color=THEME["text_white"], **kwargs):
        super().__init__(
            parent,
            text=f"  {text}  ",
            bg=bg_color,
            fg=fg_color,
            font=(THEME["font_family"], 9, "bold"),
            padx=6,
            pady=2,
            **kwargs
        )


# =============================================================================
# 1. WELCOME SCREEN
# =============================================================================
class WelcomeScreen(tk.Frame):
    """Welcome and landing screen."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg_main"])
        self.controller = controller

        # Center Container
        center_box = tk.Frame(self, bg=THEME["bg_main"])
        center_box.pack(expand=True, fill="both", padx=40, pady=30)

        # Header Badge
        badge_frame = tk.Frame(center_box, bg=THEME["bg_main"])
        badge_frame.pack(anchor="center", pady=(10, 8))
        PillBadge(badge_frame, "🎓 B.Tech 2nd-Year CSE (AIML) College Project", bg_color=THEME["primary"]).pack()

        # Title and Subtitle
        title = tk.Label(
            center_box,
            text="BRAINQUEST QUIZ PORTAL",
            font=(THEME["font_family"], 26, "bold"),
            fg=THEME["text_white"],
            bg=THEME["bg_main"]
        )
        title.pack(anchor="center", pady=(5, 4))

        subtitle = tk.Label(
            center_box,
            text="Interactive Knowledge Assessment System with Live Timer & Analytics",
            font=(THEME["font_family"], 11),
            fg=THEME["text_muted"],
            bg=THEME["bg_main"]
        )
        subtitle.pack(anchor="center", pady=(0, 20))

        # Main Student Login Card
        card = ModernCard(center_box)
        card.pack(anchor="center", fill="x", padx=100, pady=10)

        inner = card.inner

        prompt_lbl = tk.Label(
            inner,
            text="👤 Enter Candidate / Student Name:",
            font=(THEME["font_family"], 12, "bold"),
            fg=THEME["text_white"],
            bg=THEME["bg_card"]
        )
        prompt_lbl.pack(anchor="w", pady=(0, 6))

        # Name Entry Box
        entry_wrap = tk.Frame(inner, bg=THEME["border"], padx=1, pady=1)
        entry_wrap.pack(fill="x", pady=(0, 15))

        self.name_entry = tk.Entry(
            entry_wrap,
            font=(THEME["font_family"], 12),
            bg=THEME["bg_main"],
            fg=THEME["text_white"],
            insertbackground=THEME["text_white"],
            relief="flat",
            bd=0
        )
        self.name_entry.pack(fill="x", ipady=8, padx=8)
        self.name_entry.insert(0, self.controller.current_student_name)
        self.name_entry.bind("<Return>", lambda e: self.on_start_click())

        # Category Feature Badges Preview
        cats_label = tk.Label(
            inner,
            text="Featured Subject Areas:",
            font=(THEME["font_family"], 10, "bold"),
            fg=THEME["text_muted"],
            bg=THEME["bg_card"]
        )
        cats_label.pack(anchor="w", pady=(5, 6))

        pills_row = tk.Frame(inner, bg=THEME["bg_card"])
        pills_row.pack(fill="x", pady=(0, 18))

        topics = [
            ("🐍 Python", "#3B82F6"),
            ("⚙️ C++", "#8B5CF6"),
            ("🌲 Data Structures", "#10B981"),
            ("🤖 AI & ML", "#EC4899"),
            ("🌍 General Knowledge", "#F59E0B")
        ]
        for name, col in topics:
            PillBadge(pills_row, name, bg_color=col).pack(side="left", padx=4, pady=2)

        # Primary Buttons Row
        btn_row = tk.Frame(inner, bg=THEME["bg_card"])
        btn_row.pack(fill="x", pady=(10, 5))

        start_btn = tk.Button(
            btn_row,
            text="🚀 START QUIZ NOW",
            font=(THEME["font_family"], 11, "bold"),
            bg=THEME["primary"],
            fg=THEME["text_white"],
            activebackground=THEME["primary_hover"],
            activeforeground=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.on_start_click
        )
        start_btn.pack(side="left", expand=True, fill="x", padx=(0, 8))

        hist_btn = tk.Button(
            btn_row,
            text="📊 VIEW HISTORY",
            font=(THEME["font_family"], 11, "bold"),
            bg=THEME["bg_card_alt"],
            fg=THEME["text_white"],
            activebackground=THEME["border"],
            activeforeground=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: self.controller.show_screen("HistoryScreen")
        )
        hist_btn.pack(side="right", expand=True, fill="x", padx=(8, 0))

        # Bottom Info Footer
        footer_lbl = tk.Label(
            center_box,
            text="Academic Evaluation System • Python 3.11 • Tkinter Modern GUI • SQLite Storage",
            font=(THEME["font_family"], 9),
            fg=THEME["text_muted"],
            bg=THEME["bg_main"]
        )
        footer_lbl.pack(anchor="center", pady=(15, 0))

    def on_start_click(self):
        entered_name = self.name_entry.get().strip()
        if not entered_name:
            entered_name = "Candidate"
        self.controller.current_student_name = entered_name
        self.controller.show_screen("DashboardScreen")


# =============================================================================
# 2. DASHBOARD / CONFIGURATION SCREEN
# =============================================================================
class DashboardScreen(tk.Frame):
    """Quiz selection dashboard: category, difficulty, question count."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg_main"])
        self.controller = controller

        # Scrollable container or main box
        main_box = tk.Frame(self, bg=THEME["bg_main"])
        main_box.pack(fill="both", expand=True, padx=40, pady=25)

        # Header with Back Button and Greeting
        top_bar = tk.Frame(main_box, bg=THEME["bg_main"])
        top_bar.pack(fill="x", pady=(0, 15))

        back_btn = tk.Button(
            top_bar,
            text="⬅ Back to Home",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["bg_card"],
            fg=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6,
            command=lambda: self.controller.show_screen("WelcomeScreen")
        )
        back_btn.pack(side="left")

        self.welcome_user_lbl = tk.Label(
            top_bar,
            text="Welcome!",
            font=(THEME["font_family"], 14, "bold"),
            fg=THEME["accent_cyan"],
            bg=THEME["bg_main"]
        )
        self.welcome_user_lbl.pack(side="right")

        title_lbl = tk.Label(
            main_box,
            text="Quiz Configuration & Category Setup",
            font=(THEME["font_family"], 20, "bold"),
            fg=THEME["text_white"],
            bg=THEME["bg_main"]
        )
        title_lbl.pack(anchor="w", pady=(0, 15))

        # Two-column layout
        content_frame = tk.Frame(main_box, bg=THEME["bg_main"])
        content_frame.pack(fill="both", expand=True)

        # Left Column: Category Selection
        left_col = tk.Frame(content_frame, bg=THEME["bg_main"])
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 15))

        cat_card = ModernCard(left_col)
        cat_card.pack(fill="both", expand=True)
        cat_inner = cat_card.inner

        tk.Label(
            cat_inner,
            text="1. Select Quiz Category:",
            font=(THEME["font_family"], 12, "bold"),
            fg=THEME["text_white"],
            bg=THEME["bg_card"]
        ).pack(anchor="w", pady=(0, 10))

        self.selected_category_var = tk.StringVar(value="Python Programming")

        category_cards_data = [
            ("🐍 Python Programming", "Python Programming", "Syntax, OOP, Generators, GIL, Data Types"),
            ("⚙️ C++ Programming", "C++ Programming", "Pointers, Polymorphism, RAII, Smart Pointers"),
            ("🌲 Data Structures", "Data Structures", "Arrays, Trees, Heaps, Stacks, Graphs, Complexity"),
            ("🤖 AI & Machine Learning", "Artificial Intelligence and Machine Learning", "Neural Nets, Transformers, A* Search, NLP"),
            ("🌍 General Knowledge", "General Knowledge", "Science, History, Geography, Inventions"),
            ("🎲 All Categories (Mixed)", "All", "Comprehensive multidisciplinary technical challenge")
        ]

        self.category_radio_buttons = []
        for display_name, val, desc in category_cards_data:
            item_frame = tk.Frame(cat_inner, bg=THEME["bg_card_alt"], padx=10, pady=8)
            item_frame.pack(fill="x", pady=4)

            rb = tk.Radiobutton(
                item_frame,
                text=display_name,
                variable=self.selected_category_var,
                value=val,
                font=(THEME["font_family"], 11, "bold"),
                fg=THEME["text_white"],
                bg=THEME["bg_card_alt"],
                activebackground=THEME["bg_card_alt"],
                activeforeground=THEME["text_white"],
                selectcolor=THEME["bg_main"],
                relief="flat",
                cursor="hand2"
            )
            rb.pack(anchor="w")

            desc_lbl = tk.Label(
                item_frame,
                text=f"    {desc}",
                font=(THEME["font_family"], 9),
                fg=THEME["text_muted"],
                bg=THEME["bg_card_alt"]
            )
            desc_lbl.pack(anchor="w")
            self.category_radio_buttons.append(rb)

        # Right Column: Difficulty, Questions Count, and Rules
        right_col = tk.Frame(content_frame, bg=THEME["bg_main"], width=380)
        right_col.pack(side="right", fill="both", padx=(15, 0))

        diff_card = ModernCard(right_col)
        diff_card.pack(fill="x", pady=(0, 15))
        diff_inner = diff_card.inner

        tk.Label(
            diff_inner,
            text="2. Select Difficulty Level:",
            font=(THEME["font_family"], 12, "bold"),
            fg=THEME["text_white"],
            bg=THEME["bg_card"]
        ).pack(anchor="w", pady=(0, 8))

        self.selected_diff_var = tk.StringVar(value="Medium")

        diff_row = tk.Frame(diff_inner, bg=THEME["bg_card"])
        diff_row.pack(fill="x", pady=(0, 12))

        diffs = [("🟢 Easy (45s)", "Easy"), ("🟡 Medium (30s)", "Medium"), ("🔴 Hard (25s)", "Hard"), ("⚡ All", "All")]
        for text, val in diffs:
            tk.Radiobutton(
                diff_row,
                text=text,
                variable=self.selected_diff_var,
                value=val,
                font=(THEME["font_family"], 9, "bold"),
                fg=THEME["text_white"],
                bg=THEME["bg_card"],
                selectcolor=THEME["bg_main"],
                activebackground=THEME["bg_card"],
                activeforeground=THEME["text_white"],
                cursor="hand2"
            ).pack(side="left", padx=4)

        tk.Label(
            diff_inner,
            text="3. Number of Questions:",
            font=(THEME["font_family"], 12, "bold"),
            fg=THEME["text_white"],
            bg=THEME["bg_card"]
        ).pack(anchor="w", pady=(8, 6))

        self.question_count_var = tk.IntVar(value=10)
        qc_row = tk.Frame(diff_inner, bg=THEME["bg_card"])
        qc_row.pack(fill="x", pady=(0, 5))

        for num in [5, 10, 15]:
            tk.Radiobutton(
                qc_row,
                text=f"{num} Questions",
                variable=self.question_count_var,
                value=num,
                font=(THEME["font_family"], 10, "bold"),
                fg=THEME["text_white"],
                bg=THEME["bg_card"],
                selectcolor=THEME["bg_main"],
                activebackground=THEME["bg_card"],
                activeforeground=THEME["text_white"],
                cursor="hand2"
            ).pack(side="left", padx=8)

        # Rules / Instructions Card
        rules_card = ModernCard(right_col)
        rules_card.pack(fill="x", pady=(0, 15))
        rules_inner = rules_card.inner

        tk.Label(
            rules_inner,
            text="📋 Examination Rules & Guidelines:",
            font=(THEME["font_family"], 11, "bold"),
            fg=THEME["warning"],
            bg=THEME["bg_card"]
        ).pack(anchor="w", pady=(0, 4))

        rules_text = (
            "• +1 Mark for every correct answer.\n"
            "• No negative marking for wrong or unanswered questions.\n"
            "• You may navigate freely between questions.\n"
            "• When the countdown reaches 00:00, the quiz auto-submits.\n"
            "• Detailed explanations are displayed on the results review page."
        )
        tk.Label(
            rules_inner,
            text=rules_text,
            font=(THEME["font_family"], 9),
            fg=THEME["text_white"],
            bg=THEME["bg_card"],
            justify="left"
        ).pack(anchor="w")

        # Launch Button
        launch_btn = tk.Button(
            right_col,
            text="🚀 LAUNCH QUIZ NOW",
            font=(THEME["font_family"], 13, "bold"),
            bg=THEME["success"],
            fg=THEME["text_white"],
            activebackground=THEME["success_bg"],
            activeforeground=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            pady=12,
            command=self.start_quiz_session
        )
        launch_btn.pack(fill="x")

    def update_greeting(self):
        """Update personalized greeting when screen appears."""
        name = self.controller.current_student_name
        self.welcome_user_lbl.config(text=f"Candidate: {name}")

    def start_quiz_session(self):
        cat = self.selected_category_var.get()
        diff = self.selected_diff_var.get()
        limit = self.question_count_var.get()

        questions = database.fetch_questions(category=cat, difficulty=diff, limit=limit, randomize=True)
        if not questions:
            messagebox.showwarning(
                "No Questions Available",
                f"No questions matched category '{cat}' with difficulty '{diff}'. Please select different options."
            )
            return

        self.controller.init_quiz(
            category=cat,
            difficulty=diff,
            questions=questions
        )
        self.controller.show_screen("QuizScreen")


# =============================================================================
# 3. ACTIVE QUIZ SCREEN
# =============================================================================
class QuizScreen(tk.Frame):
    """The interactive question answering screen with live countdown timer."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg_main"])
        self.controller = controller

        self.questions = []
        self.current_idx = 0
        self.user_answers = {}  # {question_index: selected_option_index or None}
        self.timer_seconds_left = 0
        self.timer_active = False
        self.timer_after_id = None
        self.time_spent_seconds = 0

        # Top Bar Container
        top_bar = tk.Frame(self, bg=THEME["bg_card"], padx=20, pady=12)
        top_bar.pack(fill="x")

        # Category and Difficulty Indicators
        info_left = tk.Frame(top_bar, bg=THEME["bg_card"])
        info_left.pack(side="left")

        self.category_badge = PillBadge(info_left, "Python Programming", bg_color=THEME["primary"])
        self.category_badge.pack(side="left", padx=(0, 8))

        self.diff_badge = PillBadge(info_left, "Medium", bg_color=THEME["warning"], fg_color=THEME["text_dark"])
        self.diff_badge.pack(side="left")

        # Center Question Counter
        self.counter_lbl = tk.Label(
            top_bar,
            text="Question 1 of 10",
            font=(THEME["font_family"], 13, "bold"),
            fg=THEME["text_white"],
            bg=THEME["bg_card"]
        )
        self.counter_lbl.pack(side="left", expand=True)

        # Right Timer Badge
        timer_wrap = tk.Frame(top_bar, bg=THEME["bg_card"])
        timer_wrap.pack(side="right")

        self.timer_label = tk.Label(
            timer_wrap,
            text="⏱️ 00:00",
            font=(THEME["font_mono"], 13, "bold"),
            bg=THEME["bg_card_alt"],
            fg=THEME["accent_cyan"],
            padx=12,
            pady=4,
            relief="flat"
        )
        self.timer_label.pack(side="right")

        # Progress Bar
        self.prog_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            variable=self.prog_var,
            style="Modern.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill="x")

        # Main Question Content Area
        content_box = tk.Frame(self, bg=THEME["bg_main"], padx=40, pady=20)
        content_box.pack(fill="both", expand=True)

        # Question Card
        q_card = ModernCard(content_box)
        q_card.pack(fill="both", expand=True)
        q_inner = q_card.inner

        # Question Difficulty Tag + Prompt
        q_header = tk.Frame(q_inner, bg=THEME["bg_card"])
        q_header.pack(fill="x", pady=(0, 10))

        self.q_tag_lbl = tk.Label(
            q_header,
            text="QUESTION #1",
            font=(THEME["font_family"], 10, "bold"),
            fg=THEME["accent_cyan"],
            bg=THEME["bg_card"]
        )
        self.q_tag_lbl.pack(side="left")

        self.question_text_lbl = tk.Label(
            q_inner,
            text="Question statement will be shown here...",
            font=(THEME["font_family"], 14, "bold"),
            fg=THEME["text_white"],
            bg=THEME["bg_card"],
            wraplength=850,
            justify="left"
        )
        self.question_text_lbl.pack(anchor="w", pady=(0, 20))

        # 4 Option Card Buttons
        self.selected_opt_var = tk.IntVar(value=-1)
        self.option_frames = []
        self.option_buttons = []

        opts_container = tk.Frame(q_inner, bg=THEME["bg_card"])
        opts_container.pack(fill="both", expand=True)

        letters = ["A", "B", "C", "D"]
        for i in range(4):
            opt_frame = tk.Frame(opts_container, bg=THEME["bg_card_alt"], padx=12, pady=10)
            opt_frame.pack(fill="x", pady=5)

            rb = tk.Radiobutton(
                opt_frame,
                text=f"Option {letters[i]}",
                variable=self.selected_opt_var,
                value=i,
                font=(THEME["font_family"], 11),
                fg=THEME["text_white"],
                bg=THEME["bg_card_alt"],
                selectcolor=THEME["bg_main"],
                activebackground=THEME["bg_card_alt"],
                activeforeground=THEME["text_white"],
                cursor="hand2",
                wraplength=800,
                justify="left",
                command=self.on_option_selected
            )
            rb.pack(anchor="w", fill="x")

            self.option_frames.append(opt_frame)
            self.option_buttons.append(rb)

        # Question Navigation Strip (Palette 1..N)
        palette_card = ModernCard(content_box, bg=THEME["bg_card_alt"], border_color=THEME["border"])
        palette_card.pack(fill="x", pady=(12, 0))
        self.palette_inner = palette_card.inner
        self.palette_buttons = []

        # Bottom Bar: Navigation and Submit
        bottom_bar = tk.Frame(self, bg=THEME["bg_card"], padx=25, pady=12)
        bottom_bar.pack(fill="x")

        self.prev_btn = tk.Button(
            bottom_bar,
            text="⏮ Previous",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["bg_card_alt"],
            fg=THEME["text_white"],
            activebackground=THEME["border"],
            activeforeground=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=8,
            command=self.go_prev
        )
        self.prev_btn.pack(side="left", padx=(0, 8))

        self.clear_btn = tk.Button(
            bottom_bar,
            text="🧹 Clear Choice",
            font=(THEME["font_family"], 10),
            bg=THEME["bg_card_alt"],
            fg=THEME["text_muted"],
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8,
            command=self.clear_current_choice
        )
        self.clear_btn.pack(side="left")

        self.submit_btn = tk.Button(
            bottom_bar,
            text="✅ Submit Quiz",
            font=(THEME["font_family"], 11, "bold"),
            bg=THEME["success"],
            fg=THEME["text_white"],
            activebackground=THEME["success_bg"],
            activeforeground=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=8,
            command=self.confirm_and_submit
        )
        self.submit_btn.pack(side="right")

        self.next_btn = tk.Button(
            bottom_bar,
            text="Next ⏭",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["primary"],
            fg=THEME["text_white"],
            activebackground=THEME["primary_hover"],
            activeforeground=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=8,
            command=self.go_next
        )
        self.next_btn.pack(side="right", padx=(0, 10))

    def setup_quiz_data(self, category, difficulty, questions):
        """Initializes state for a new active quiz."""
        self.questions = questions
        self.current_idx = 0
        self.user_answers = {i: None for i in range(len(questions))}
        self.time_spent_seconds = 0

        # Calculate total timer based on difficulty and number of questions
        time_per_q = quiz_data.TIME_PER_QUESTION.get(difficulty, 30)
        self.timer_seconds_left = len(questions) * time_per_q

        # Update category/diff badges
        self.category_badge.config(text=f"  {category}  ")
        diff_color = THEME["success"] if difficulty == "Easy" else (THEME["warning"] if difficulty == "Medium" else THEME["danger"])
        self.diff_badge.config(text=f"  {difficulty}  ", bg=diff_color)

        # Build question palette buttons
        for widget in self.palette_inner.winfo_children():
            widget.destroy()
        self.palette_buttons = []

        tk.Label(
            self.palette_inner,
            text="Question Palette:",
            font=(THEME["font_family"], 9, "bold"),
            fg=THEME["text_muted"],
            bg=THEME["bg_card_alt"]
        ).pack(side="left", padx=(0, 8))

        for idx in range(len(questions)):
            btn = tk.Button(
                self.palette_inner,
                text=str(idx + 1),
                font=(THEME["font_family"], 9, "bold"),
                width=3,
                relief="flat",
                cursor="hand2",
                command=lambda target_idx=idx: self.jump_to_question(target_idx)
            )
            btn.pack(side="left", padx=2)
            self.palette_buttons.append(btn)

        self.start_countdown_timer()
        self.render_current_question()

    def start_countdown_timer(self):
        """Starts or restarts the 1-second interval countdown timer."""
        if self.timer_after_id:
            self.after_cancel(self.timer_after_id)
            self.timer_after_id = None

        self.timer_active = True
        self.tick_timer()

    def stop_countdown_timer(self):
        """Stops the countdown timer cleanly."""
        self.timer_active = False
        if self.timer_after_id:
            self.after_cancel(self.timer_after_id)
            self.timer_after_id = None

    def tick_timer(self):
        """Clock tick executed every second."""
        if not self.timer_active:
            return

        minutes = self.timer_seconds_left // 60
        secs = self.timer_seconds_left % 60
        time_str = f"⏱️ {minutes:02d}:{secs:02d}"
        self.timer_label.config(text=time_str)

        # Color changes based on remaining time
        if self.timer_seconds_left <= 10:
            self.timer_label.config(fg=THEME["danger"], bg=THEME["danger_bg"])
        elif self.timer_seconds_left <= 30:
            self.timer_label.config(fg=THEME["warning"], bg=THEME["bg_card_alt"])
        else:
            self.timer_label.config(fg=THEME["accent_cyan"], bg=THEME["bg_card_alt"])

        if self.timer_seconds_left <= 0:
            self.stop_countdown_timer()
            messagebox.showinfo(
                "Time Expired!",
                "⏰ Time is up! Your quiz answers are being automatically submitted."
            )
            self.finalize_and_submit()
            return

        self.timer_seconds_left -= 1
        self.time_spent_seconds += 1
        self.timer_after_id = self.after(1000, self.tick_timer)

    def render_current_question(self):
        """Renders the question at self.current_idx."""
        if not self.questions or self.current_idx < 0 or self.current_idx >= len(self.questions):
            return

        q = self.questions[self.current_idx]
        total = len(self.questions)

        # Update Counter & Progress Bar
        self.counter_lbl.config(text=f"Question {self.current_idx + 1} of {total}")
        progress_val = ((self.current_idx + 1) / total) * 100
        self.prog_var.set(progress_val)

        # Question header & text
        self.q_tag_lbl.config(text=f"QUESTION #{self.current_idx + 1}  •  {q.get('difficulty', 'Medium').upper()}")
        self.question_text_lbl.config(text=q["question"])

        # Selected answer
        chosen = self.user_answers.get(self.current_idx)
        if chosen is None:
            self.selected_opt_var.set(-1)
        else:
            self.selected_opt_var.set(chosen)

        # Render options
        letters = ["A", "B", "C", "D"]
        for i in range(4):
            opt_text = q["options"][i]
            self.option_buttons[i].config(text=f"[{letters[i]}]  {opt_text}")
            self.update_option_frame_style(i, is_selected=(chosen == i))

        # Update navigation buttons
        self.prev_btn.config(state="normal" if self.current_idx > 0 else "disabled")
        if self.current_idx == total - 1:
            self.next_btn.config(text="Submit 🏁", bg=THEME["success"])
        else:
            self.next_btn.config(text="Next ⏭", bg=THEME["primary"])

        # Update palette buttons colors
        self.update_palette_colors()

    def update_option_frame_style(self, opt_idx, is_selected=False):
        """Visually highlights selected option card."""
        frame = self.option_frames[opt_idx]
        rb = self.option_buttons[opt_idx]
        if is_selected:
            frame.config(bg=THEME["primary"])
            rb.config(bg=THEME["primary"], activebackground=THEME["primary"])
        else:
            frame.config(bg=THEME["bg_card_alt"])
            rb.config(bg=THEME["bg_card_alt"], activebackground=THEME["bg_card_alt"])

    def on_option_selected(self):
        """Triggered when user clicks an option radio button."""
        val = self.selected_opt_var.get()
        self.user_answers[self.current_idx] = val
        for i in range(4):
            self.update_option_frame_style(i, is_selected=(i == val))
        self.update_palette_colors()

    def clear_current_choice(self):
        """Clears the currently selected choice."""
        self.selected_opt_var.set(-1)
        self.user_answers[self.current_idx] = None
        for i in range(4):
            self.update_option_frame_style(i, is_selected=False)
        self.update_palette_colors()

    def update_palette_colors(self):
        """Updates the question palette indicators (answered, unanswered, current)."""
        for idx, btn in enumerate(self.palette_buttons):
            has_ans = self.user_answers.get(idx) is not None
            is_current = (idx == self.current_idx)

            if is_current:
                btn.config(bg=THEME["accent_cyan"], fg=THEME["text_dark"])
            elif has_ans:
                btn.config(bg=THEME["success"], fg=THEME["text_white"])
            else:
                btn.config(bg=THEME["bg_card"], fg=THEME["text_muted"])

    def go_prev(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            self.render_current_question()

    def go_next(self):
        if self.current_idx < len(self.questions) - 1:
            self.current_idx += 1
            self.render_current_question()
        else:
            self.confirm_and_submit()

    def jump_to_question(self, target_idx):
        if 0 <= target_idx < len(self.questions):
            self.current_idx = target_idx
            self.render_current_question()

    def confirm_and_submit(self):
        """Confirms submission, checking for unanswered questions."""
        unanswered = sum(1 for ans in self.user_answers.values() if ans is None)
        total = len(self.questions)

        if unanswered > 0:
            msg = f"You have {unanswered} unanswered question(s) out of {total}.\n\nAre you sure you want to finish and submit the quiz?"
            confirmed = messagebox.askyesno("Confirm Quiz Submission", msg)
            if not confirmed:
                return

        self.finalize_and_submit()

    def finalize_and_submit(self):
        """Computes score, records attempt in database, navigates to results."""
        self.stop_countdown_timer()

        # Score calculation
        score = 0
        total = len(self.questions)
        detailed_results = []

        for idx, q in enumerate(self.questions):
            user_pick = self.user_answers.get(idx)
            correct_idx = q["correct_index"]
            is_correct = (user_pick is not None and user_pick == correct_idx)

            if is_correct:
                score += 1

            detailed_results.append({
                "question": q["question"],
                "options": q["options"],
                "correct_index": correct_idx,
                "user_choice": user_pick,
                "is_correct": is_correct,
                "explanation": q["explanation"],
                "category": q["category"],
                "difficulty": q["difficulty"]
            })

        # Record in database
        cat = self.questions[0]["category"] if self.questions else "General"
        diff = self.questions[0]["difficulty"] if self.questions else "Medium"
        attempt_id = database.record_attempt(
            student_name=self.controller.current_student_name,
            category=cat,
            difficulty=diff,
            score=score,
            total_questions=total,
            time_taken_seconds=self.time_spent_seconds
        )

        self.controller.display_quiz_results(
            attempt_id=attempt_id,
            category=cat,
            difficulty=diff,
            score=score,
            total=total,
            time_spent_seconds=self.time_spent_seconds,
            detailed_results=detailed_results
        )
        self.controller.show_screen("ResultsScreen")


# =============================================================================
# 4. RESULTS & ANALYTICS SCREEN
# =============================================================================
class ResultsScreen(tk.Frame):
    """Displays comprehensive performance scorecard and action controls."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg_main"])
        self.controller = controller
        self.cached_results = []

        center_box = tk.Frame(self, bg=THEME["bg_main"], padx=40, pady=25)
        center_box.pack(fill="both", expand=True)

        # Header Pill & Congratulatory Title
        top_bar = tk.Frame(center_box, bg=THEME["bg_main"])
        top_bar.pack(anchor="center", pady=(0, 10))

        self.celebration_badge = PillBadge(top_bar, "🎉 Quiz Successfully Completed!", bg_color=THEME["primary"])
        self.celebration_badge.pack(anchor="center", pady=(0, 6))

        self.candidate_name_lbl = tk.Label(
            top_bar,
            text="Performance Report for Candidate",
            font=(THEME["font_family"], 20, "bold"),
            fg=THEME["text_white"],
            bg=THEME["bg_main"]
        )
        self.candidate_name_lbl.pack(anchor="center")

        # Big Score Card
        score_card = ModernCard(center_box)
        score_card.pack(fill="x", padx=60, pady=10)
        s_inner = score_card.inner

        # Score percentage & Grade
        score_row = tk.Frame(s_inner, bg=THEME["bg_card"])
        score_row.pack(fill="x", pady=5)

        self.pct_display_lbl = tk.Label(
            score_row,
            text="80.0%",
            font=(THEME["font_family"], 38, "bold"),
            fg=THEME["success"],
            bg=THEME["bg_card"]
        )
        self.pct_display_lbl.pack(side="left", padx=20)

        grade_box = tk.Frame(score_row, bg=THEME["bg_card"])
        grade_box.pack(side="left", fill="both", expand=True)

        self.score_fraction_lbl = tk.Label(
            grade_box,
            text="Score: 8 / 10 Marks",
            font=(THEME["font_family"], 14, "bold"),
            fg=THEME["text_white"],
            bg=THEME["bg_card"]
        )
        self.score_fraction_lbl.pack(anchor="w")

        self.grade_lbl = tk.Label(
            grade_box,
            text="Academic Standing: Grade A (Excellent)",
            font=(THEME["font_family"], 11),
            fg=THEME["accent_cyan"],
            bg=THEME["bg_card"]
        )
        self.grade_lbl.pack(anchor="w", pady=(2, 0))

        # 4 Metric Cards Row
        metrics_row = tk.Frame(center_box, bg=THEME["bg_main"])
        metrics_row.pack(fill="x", padx=60, pady=15)

        self.metric_widgets = {}
        metric_configs = [
            ("correct", "✅ Correct", "0", THEME["success"]),
            ("incorrect", "❌ Incorrect", "0", THEME["danger"]),
            ("unanswered", "⚪ Skipped", "0", THEME["text_muted"]),
            ("time", "⏱️ Time Taken", "00:00", THEME["accent_cyan"])
        ]

        for key, title, def_val, color in metric_configs:
            m_card = tk.Frame(metrics_row, bg=THEME["bg_card_alt"], padx=15, pady=12, relief="flat")
            m_card.pack(side="left", expand=True, fill="x", padx=6)

            tk.Label(
                m_card,
                text=title,
                font=(THEME["font_family"], 10, "bold"),
                fg=THEME["text_muted"],
                bg=THEME["bg_card_alt"]
            ).pack(anchor="center")

            val_lbl = tk.Label(
                m_card,
                text=def_val,
                font=(THEME["font_family"], 16, "bold"),
                fg=color,
                bg=THEME["bg_card_alt"]
            )
            val_lbl.pack(anchor="center", pady=(4, 0))
            self.metric_widgets[key] = val_lbl

        # Action Buttons
        actions_frame = tk.Frame(center_box, bg=THEME["bg_main"])
        actions_frame.pack(fill="x", padx=60, pady=15)

        review_btn = tk.Button(
            actions_frame,
            text="🔍 Review Answers & Explanations",
            font=(THEME["font_family"], 11, "bold"),
            bg=THEME["primary"],
            fg=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=10,
            command=self.open_review_modal
        )
        review_btn.pack(side="left", expand=True, fill="x", padx=4)

        retake_btn = tk.Button(
            actions_frame,
            text="🔄 Retake Quiz",
            font=(THEME["font_family"], 11, "bold"),
            bg=THEME["bg_card_alt"],
            fg=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=10,
            command=lambda: self.controller.show_screen("DashboardScreen")
        )
        retake_btn.pack(side="left", expand=True, fill="x", padx=4)

        history_btn = tk.Button(
            actions_frame,
            text="📊 View History",
            font=(THEME["font_family"], 11, "bold"),
            bg=THEME["bg_card_alt"],
            fg=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=10,
            command=lambda: self.controller.show_screen("HistoryScreen")
        )
        history_btn.pack(side="left", expand=True, fill="x", padx=4)

        home_btn = tk.Button(
            actions_frame,
            text="🏠 Back to Home",
            font=(THEME["font_family"], 11, "bold"),
            bg=THEME["border"],
            fg=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=10,
            command=lambda: self.controller.show_screen("WelcomeScreen")
        )
        home_btn.pack(side="left", expand=True, fill="x", padx=4)

    def populate_results(self, attempt_id, category, difficulty, score, total, time_spent_seconds, detailed_results):
        """Fills results widgets with calculated test data."""
        self.cached_results = detailed_results
        student_name = self.controller.current_student_name
        self.candidate_name_lbl.config(text=f"Report Card: {student_name}")

        percentage = round((score / total) * 100, 1)
        self.pct_display_lbl.config(text=f"{percentage}%")
        if percentage >= 75:
            self.pct_display_lbl.config(fg=THEME["success"])
        elif percentage >= 50:
            self.pct_display_lbl.config(fg=THEME["warning"])
        else:
            self.pct_display_lbl.config(fg=THEME["danger"])

        self.score_fraction_lbl.config(text=f"Score: {score} out of {total} Questions Correct")
        grade_text = database.calculate_grade(percentage)
        self.grade_lbl.config(text=f"Standing: {grade_text}")

        # Metrics
        correct_count = sum(1 for r in detailed_results if r["is_correct"])
        unanswered_count = sum(1 for r in detailed_results if r["user_choice"] is None)
        incorrect_count = total - correct_count - unanswered_count

        self.metric_widgets["correct"].config(text=str(correct_count))
        self.metric_widgets["incorrect"].config(text=str(incorrect_count))
        self.metric_widgets["unanswered"].config(text=str(unanswered_count))

        mins = time_spent_seconds // 60
        secs = time_spent_seconds % 60
        self.metric_widgets["time"].config(text=f"{mins:02d}m {secs:02d}s")

    def open_review_modal(self):
        """Launches the dedicated scrollable review dialog."""
        ReviewDialog(self, self.cached_results)


# =============================================================================
# 5. DETAILED ANSWER REVIEW WINDOW
# =============================================================================
class ReviewDialog(tk.Toplevel):
    """Scrollable modal displaying questions, answers, and explanations."""
    def __init__(self, parent, detailed_results):
        super().__init__(parent)
        self.title("Detailed Answer Review & Technical Explanations")
        self.geometry("920x650")
        self.configure(bg=THEME["bg_main"])
        self.detailed_results = detailed_results

        # Top Bar
        top_bar = tk.Frame(self, bg=THEME["bg_card"], padx=20, pady=12)
        top_bar.pack(fill="x")

        tk.Label(
            top_bar,
            text="📖 Question by Question Technical Breakdown",
            font=(THEME["font_family"], 14, "bold"),
            fg=THEME["text_white"],
            bg=THEME["bg_card"]
        ).pack(side="left")

        close_btn = tk.Button(
            top_bar,
            text="Close Review ✕",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["danger"],
            fg=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.destroy
        )
        close_btn.pack(side="right")

        # Scrollable Canvas
        canvas_wrap = tk.Frame(self, bg=THEME["bg_main"])
        canvas_wrap.pack(fill="both", expand=True, padx=20, pady=15)

        self.canvas = tk.Canvas(canvas_wrap, bg=THEME["bg_main"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_wrap, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=THEME["bg_main"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=860)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel scroll binding
        self.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        # Render questions
        letters = ["A", "B", "C", "D"]
        for idx, res in enumerate(self.detailed_results):
            card = ModernCard(self.scrollable_frame)
            card.pack(fill="x", pady=8)
            inner = card.inner

            # Header row
            h_row = tk.Frame(inner, bg=THEME["bg_card"])
            h_row.pack(fill="x", pady=(0, 6))

            status_text = "✅ CORRECT" if res["is_correct"] else ("⚪ UNANSWERED" if res["user_choice"] is None else "❌ INCORRECT")
            status_color = THEME["success"] if res["is_correct"] else (THEME["text_muted"] if res["user_choice"] is None else THEME["danger"])

            PillBadge(h_row, f"Q{idx + 1} • {status_text}", bg_color=status_color).pack(side="left")
            PillBadge(h_row, res.get("difficulty", "Medium"), bg_color=THEME["bg_card_alt"]).pack(side="left", padx=8)

            # Question text
            tk.Label(
                inner,
                text=res["question"],
                font=(THEME["font_family"], 11, "bold"),
                fg=THEME["text_white"],
                bg=THEME["bg_card"],
                wraplength=820,
                justify="left"
            ).pack(anchor="w", pady=(4, 10))

            # Options listing
            for o_idx in range(4):
                opt_str = f"[{letters[o_idx]}] {res['options'][o_idx]}"
                is_correct_opt = (o_idx == res["correct_index"])
                is_user_opt = (o_idx == res["user_choice"])

                opt_bg = THEME["bg_card_alt"]
                opt_fg = THEME["text_white"]

                tag_note = ""
                if is_correct_opt and is_user_opt:
                    opt_bg = THEME["success_bg"]
                    opt_fg = THEME["success"]
                    tag_note = "  (Your Choice - Correct!)"
                elif is_correct_opt:
                    opt_bg = THEME["success_bg"]
                    opt_fg = THEME["success"]
                    tag_note = "  (Correct Answer)"
                elif is_user_opt:
                    opt_bg = THEME["danger_bg"]
                    opt_fg = THEME["danger"]
                    tag_note = "  (Your Choice - Incorrect)"

                opt_box = tk.Frame(inner, bg=opt_bg, padx=8, pady=4)
                opt_box.pack(fill="x", pady=2)

                tk.Label(
                    opt_box,
                    text=f"{opt_str}{tag_note}",
                    font=(THEME["font_family"], 9, "bold" if (is_correct_opt or is_user_opt) else "normal"),
                    fg=opt_fg,
                    bg=opt_bg
                ).pack(anchor="w")

            # Explanation box
            exp_box = tk.Frame(inner, bg=THEME["bg_main"], padx=10, pady=8)
            exp_box.pack(fill="x", pady=(10, 0))

            tk.Label(
                exp_box,
                text=f"💡 Concept Explanation: {res['explanation']}",
                font=(THEME["font_family"], 9),
                fg=THEME["accent_cyan"],
                bg=THEME["bg_main"],
                wraplength=800,
                justify="left"
            ).pack(anchor="w")


# =============================================================================
# 6. HISTORY & ANALYTICS SCREEN
# =============================================================================
class HistoryScreen(tk.Frame):
    """View previous quiz attempts, score history, and summary analytics."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg_main"])
        self.controller = controller

        main_box = tk.Frame(self, bg=THEME["bg_main"], padx=40, pady=25)
        main_box.pack(fill="both", expand=True)

        # Top Bar
        top_bar = tk.Frame(main_box, bg=THEME["bg_main"])
        top_bar.pack(fill="x", pady=(0, 15))

        back_btn = tk.Button(
            top_bar,
            text="⬅ Back to Dashboard",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["bg_card"],
            fg=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6,
            command=lambda: self.controller.show_screen("DashboardScreen")
        )
        back_btn.pack(side="left")

        title_lbl = tk.Label(
            top_bar,
            text="Historical Quiz Records & Performance Analytics",
            font=(THEME["font_family"], 16, "bold"),
            fg=THEME["text_white"],
            bg=THEME["bg_main"]
        )
        title_lbl.pack(side="left", padx=20)

        # Overview Stats Cards
        self.stats_row = tk.Frame(main_box, bg=THEME["bg_main"])
        self.stats_row.pack(fill="x", pady=(0, 15))

        self.stat_cards = {}
        items = [
            ("total_attempts", "Total Attempts", "0", THEME["primary_hover"]),
            ("avg_percentage", "Avg Score", "0%", THEME["warning"]),
            ("max_percentage", "Best Score", "0%", THEME["success"]),
            ("most_popular_category", "Top Category", "None", THEME["accent_cyan"])
        ]
        for key, title, def_val, col in items:
            box = tk.Frame(self.stats_row, bg=THEME["bg_card"], padx=14, pady=10)
            box.pack(side="left", expand=True, fill="x", padx=4)

            tk.Label(box, text=title, font=(THEME["font_family"], 9, "bold"), fg=THEME["text_muted"], bg=THEME["bg_card"]).pack(anchor="w")
            lbl = tk.Label(box, text=def_val, font=(THEME["font_family"], 13, "bold"), fg=col, bg=THEME["bg_card"])
            lbl.pack(anchor="w", pady=(2, 0))
            self.stat_cards[key] = lbl

        # Filters Bar
        filters_bar = tk.Frame(main_box, bg=THEME["bg_card"], padx=12, pady=8)
        filters_bar.pack(fill="x", pady=(0, 10))

        tk.Label(filters_bar, text="Filter Category:", font=(THEME["font_family"], 10, "bold"), fg=THEME["text_white"], bg=THEME["bg_card"]).pack(side="left", padx=(0, 6))

        self.filter_cat_var = tk.StringVar(value="All")
        cats = ["All"] + quiz_data.CATEGORIES
        cat_menu = ttk.Combobox(filters_bar, textvariable=self.filter_cat_var, values=cats, state="readonly", width=22)
        cat_menu.pack(side="left", padx=(0, 15))
        cat_menu.bind("<<ComboboxSelected>>", lambda e: self.load_history_records())

        tk.Label(filters_bar, text="Candidate Search:", font=(THEME["font_family"], 10, "bold"), fg=THEME["text_white"], bg=THEME["bg_card"]).pack(side="left", padx=(0, 6))

        self.search_entry = tk.Entry(filters_bar, font=(THEME["font_family"], 10), bg=THEME["bg_main"], fg=THEME["text_white"], width=18)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_history_records())

        refresh_btn = tk.Button(
            filters_bar,
            text="🔄 Refresh",
            font=(THEME["font_family"], 9, "bold"),
            bg=THEME["bg_card_alt"],
            fg=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=10,
            command=self.load_history_records
        )
        refresh_btn.pack(side="left")

        clear_btn = tk.Button(
            filters_bar,
            text="🗑️ Clear All History",
            font=(THEME["font_family"], 9, "bold"),
            bg=THEME["danger"],
            fg=THEME["text_white"],
            relief="flat",
            cursor="hand2",
            padx=10,
            command=self.clear_all_history
        )
        clear_btn.pack(side="right")

        # Treeview Table
        table_frame = tk.Frame(main_box, bg=THEME["bg_card"])
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "name", "category", "difficulty", "score", "percentage", "grade", "time", "date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Modern.Treeview")

        headings = {
            "id": ("ID", 40),
            "name": ("Candidate Name", 130),
            "category": ("Category", 180),
            "difficulty": ("Difficulty", 80),
            "score": ("Score", 70),
            "percentage": ("Percentage", 80),
            "grade": ("Grade", 140),
            "time": ("Time Spent", 80),
            "date": ("Timestamp", 140)
        }

        for col, (title, width) in headings.items():
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, anchor="center" if col in ("id", "difficulty", "score", "percentage", "time") else "w")

        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

    def load_history_records(self):
        """Fetches and populates history rows and overview metrics."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        cat_filter = self.filter_cat_var.get()
        student_filter = self.search_entry.get().strip()

        history = database.get_quiz_history(
            limit=100,
            category_filter=cat_filter,
            student_filter=student_filter
        )

        for row in history:
            mins = row["time_taken_seconds"] // 60
            secs = row["time_taken_seconds"] % 60
            time_str = f"{mins:02d}m {secs:02d}s"

            self.tree.insert("", "end", values=(
                row["id"],
                row["student_name"],
                row["category"],
                row["difficulty"],
                f"{row['score']} / {row['total_questions']}",
                f"{row['percentage']}%",
                row["grade"],
                time_str,
                row["timestamp"]
            ))

        # Update stats
        summary = database.get_analytics_summary()
        self.stat_cards["total_attempts"].config(text=str(summary["total_attempts"]))
        self.stat_cards["avg_percentage"].config(text=f"{summary['avg_percentage']}%")
        self.stat_cards["max_percentage"].config(text=f"{summary['max_percentage']}%")
        self.stat_cards["most_popular_category"].config(text=summary["most_popular_category"])

    def clear_all_history(self):
        """Prompt and erase all history records."""
        confirm = messagebox.askyesno(
            "Clear History",
            "Are you sure you want to delete all historical quiz attempt records? This action cannot be undone."
        )
        if confirm:
            database.clear_all_history()
            self.load_history_records()
            messagebox.showinfo("History Cleared", "All quiz history records have been successfully deleted.")
