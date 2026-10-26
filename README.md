# 🧠 BrainQuest — Smart Python Technical Quiz & Evaluation Portal
### B.Tech 2nd-Year Computer Science and Engineering (AI & ML) Project

---

## 📌 Project Overview
**BrainQuest** is a modern, modular, and interactive desktop technical quiz application engineered using **Python 3**, **Tkinter (ttk)**, and **SQLite3**. Designed as a comprehensive college evaluation system, it enables students to test their conceptual and analytical knowledge across core computer science and engineering disciplines, answer randomized multiple-choice questions under timed conditions, track live progress, and review detailed theoretical explanations post-submission.

All quiz attempts, scores, timestamps, and performance metrics are stored persistently in a local SQLite database, allowing candidates and academic evaluators to analyze historical performance and academic trends.

---

## 🌟 Key Highlights & Features

1. **🎨 Modern & Responsive UI (Dark Slate / Indigo Theme)**
   - Custom card-based layout inspired by modern web assessment platforms.
   - High-contrast visual cues (Emerald for success, Crimson for alerts, Amber for warnings, Cyan for timers).
   - Designed to run smoothly on Windows 10/11 laptop displays (default geometry: 1020x720, responsive and resizable).

2. **📚 Comprehensive Technical Question Bank (75 Curated Questions)**
   - **5 Major Domains**:
     - 🐍 **Python Programming** (Decorators, Metaclasses, GIL, Generators, Comprehensions, Immutability)
     - ⚙️ **C++ Programming** (Pointers, Polymorphism, Virtual Destructors, RAII, Smart Pointers, Move Semantics)
     - 🌲 **Data Structures** (BST, AVL Trees, Red-Black Trees, DSU, Tries, Hash Tables, Asymptotic Complexity)
     - 🤖 **Artificial Intelligence & Machine Learning** (Supervised/Unsupervised, Neural Networks, Transformers, A* Search, GANs, Regularization)
     - 🌍 **General Knowledge & Science** (Physics, Inventions, World History, IT Milestones, Geography)
   - **3 Difficulty Tiers**: Easy, Medium, and Hard (with dynamic time allocation per question).
   - **Full Explanations**: Every question includes a detailed pedagogical explanation explaining why the correct option is right.

3. **⏱️ Real-Time Countdown Timer & Auto-Submit**
   - Dynamic time calculation based on selected difficulty level.
   - Visual color shifts (Cyan ➔ Amber at $\le$ 30s ➔ Pulsing Red at $\le$ 10s).
   - Automatic quiz termination and submission when the timer reaches `00:00`.

4. **🔄 Flexible Navigation & Question Palette**
   - Jump directly to any question using the interactive 1-to-N **Question Palette**.
   - Color-coded palette status: Green (Answered), Dark Slate (Unanswered), Cyan (Current).
   - "Next", "Previous", and "Clear Choice" controls.
   - Candidates can freely modify or clear answers at any time prior to submission.
   - Unanswered question detection with confirmation dialog on submit.

5. **📊 In-Depth Results & Performance Analytics**
   - Real-time score calculation and percentage scoring.
   - Letter grades with academic remarks: $A^+$ (Outstanding), $A$ (Excellent), $B^+$ (Very Good), etc.
   - Metric summary cards: Total Questions, Correct Answers, Incorrect Answers, Time Elapsed.
   - Dedicated **Scrollable Review Window** displaying question text, candidate's choice, correct choice, and in-depth concept notes.

6. **💾 Persistent SQLite Database Storage**
   - Relational database schema with `questions` and `quiz_attempts` tables.
   - Automatic seeding of questions on first boot.
   - Searchable and filterable **History Table (Treeview)** with candidate search and category filter.
   - High-level analytics: Total Attempts, Overall Average Score, Highest Score, and Most Popular Category.

---

## 🗂️ Project Directory Structure

```text
python_quiz_app/
│
├── main.py               # Application entry point; initializes GUI and screen router
├── ui.py                 # User Interface screens (Welcome, Dashboard, Quiz, Results, History, Review)
├── database.py           # SQLite manager (connection, migrations, seeding, queries, analytics)
├── quiz_data.py          # Question bank containing 75 questions with options and explanations
├── requirements.txt      # Dependency specification (Standard Library, zero external packages)
├── run_app.bat           # One-click Windows batch launcher
├── test_quiz_app.py      # Automated unit test suite verifying data, logic, and GUI
├── quiz_portal.db        # SQLite database file (generated automatically on first run)
└── README.md             # Complete college project documentation
```

---

## 🚀 How to Run the Project on Localhost (Web Version)

The application includes a web edition built with Flask and Jinja2 that runs on `http://localhost:5000` with the same questions, live timer, scoring, and SQLite history database.

### Method 1: One-Click Web Launcher (Easiest)
Simply double-click **`run_web.bat`** in the project directory. It launches the local web server and starts listening at:
👉 **[http://localhost:5000](http://localhost:5000)** (or [http://127.0.0.1:5000](http://127.0.0.1:5000))

### Method 2: From VS Code / Windows Terminal
1. Open the project folder in VS Code or Terminal:
   ```powershell
   cd C:\Users\mansi\.gemini\antigravity\scratch\python_quiz_app
   ```
2. Start the localhost server:
   ```powershell
   python app.py
   ```
3. Open your browser (Chrome, Edge, Firefox) and navigate to:
   ```text
   http://localhost:5000
   ```

---

## 🖥️ How to Run the Desktop Tkinter Application

If you or your college evaluators prefer the native desktop window interface:

### Method 1: One-Click Desktop Launcher
Double-click **`run_app.bat`** in the `python_quiz_app` folder.

### Method 2: From Terminal
```powershell
python main.py
```

### Method 3: Running Automated Tests
To run the automated test suite verifying all database operations, quiz scoring, and UI transitions:
```powershell
python -m unittest test_quiz_app.py
```

---

## 🧩 Architectural Design & Python Concepts Used

| Module | Core Responsibilities | Key Python Concepts Employed |
| :--- | :--- | :--- |
| `main.py` | App entry point, master window geometry, lifecycle management. | Object-Oriented Programming (OOP), Tkinter subclassing (`tk.Tk`), Stack-based frame routing (`tkraise`), protocol handlers (`WM_DELETE_WINDOW`). |
| `quiz_data.py` | 75 curated technical questions, domain categories, timing configs. | Dictionaries, Lists of Objects, Constant Declarations, Filtering functions with list comprehensions. |
| `database.py` | SQLite connectivity, table schemas, question seeding, attempt logging. | Context managers, Parameterized SQL queries (preventing SQL injection), Row factories, Aggregation functions (`COUNT`, `AVG`, `MAX`, `GROUP BY`), Datetime formatting. |
| `ui.py` | All graphical visual screens, theme constants, custom widgets. | Tkinter widgets (`Frame`, `Label`, `Button`, `Radiobutton`, `Entry`), `ttk.Treeview`, `ttk.Progressbar`, `Canvas` with scrollable regions, event binding (`<Return>`, `<KeyRelease>`, `<MouseWheel>`), `after()` timer loops. |
| `test_quiz_app.py` | Unit testing and automated flow verification. | `unittest.TestCase`, test lifecycle fixtures (`setUpClass`, `tearDownClass`), assertions (`assertEqual`, `assertGreaterEqual`, `assertIn`). |

---

## 📸 Application Screen Flow & Visual Hierarchy

```text
+-----------------------------------------------------------------------------------+
|                              WELCOME SCREEN                                       |
|  [🎓 B.Tech 2nd-Year CSE (AIML) College Project]                                  |
|  BRAINQUEST QUIZ PORTAL                                                           |
|  Enter Student Name: [_______________________]                                    |
|  Featured Topics: [🐍 Python] [⚙️ C++] [🌲 Data Structures] [🤖 AI & ML] [🌍 GK]  |
|                 [ 🚀 START QUIZ NOW ]      [ 📊 VIEW HISTORY ]                    |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                            DASHBOARD SCREEN                                       |
|  1. Select Category:               2. Difficulty:       3. Questions:             |
|     (•) Python Programming            ( ) Easy (45s)       ( ) 5 Questions        |
|     ( ) C++ Programming               (•) Medium (30s)     (•) 10 Questions       |
|     ( ) Data Structures               ( ) Hard (25s)       ( ) 15 Questions       |
|     ( ) AI & Machine Learning                                                     |
|     ( ) General Knowledge                                                         |
|                                                                                   |
|  [ 📋 Examination Rules & Scoring Guidelines Card ]                               |
|                           [ 🚀 LAUNCH QUIZ NOW ]                                  |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                              ACTIVE QUIZ SCREEN                                   |
|  [Python Programming]  [Medium]       Question 3 of 10             [⏱️ 04:32]     |
|  [========================== PROGRESS BAR ===============================] 30%    |
|                                                                                   |
|  QUESTION #3 • MEDIUM                                                             |
|  Which of the following data types in Python is IMMUTABLE?                        |
|                                                                                   |
|  ( ) [A] List                                                                     |
|  ( ) [B] Dictionary                                                               |
|  ( ) [C] Set                                                                      |
|  (•) [D] Tuple                                                                    |
|                                                                                   |
|  Question Palette: [1✓] [2✓] [3*] [4 ] [5 ] [6 ] [7 ] [8 ] [9 ] [10]              |
|  [⏮ Previous]   [🧹 Clear Choice]             [Next ⏭]    [✅ Submit Quiz]       |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                              RESULTS SCREEN                                       |
|  🎉 Quiz Successfully Completed!  Report Card: Mansi Sharma                       |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |  80.0%    Score: 8 out of 10 Questions Correct                              |  |
|  |           Standing: Grade A (Excellent)                                     |  |
|  +-----------------------------------------------------------------------------+  |
|  [ Correct: 8 ]   [ Incorrect: 1 ]   [ Skipped: 1 ]   [ Time: 02m 14s ]           |
|                                                                                   |
|  [🔍 Review Answers & Explanations]  [🔄 Retake Quiz]  [📊 View History]          |
+-----------------------------------------------------------------------------------+
```

---

## 🎓 College Project Report Outline (For Submission)

### 1. Title Page
- Project Title: **BrainQuest — Technical Quiz & Examination Portal**
- Course: Bachelor of Technology (B.Tech) in Computer Science & Engineering (AIML)
- Academic Year: 2nd Year (Semester IV)
- Submitted by: [Student Name & Roll Number]
- Guided by: [Faculty Supervisor / Department of CSE]

### 2. Certificate of Originality & Acknowledgements
- Departmental verification certificate and gratitude to mentors and laboratory staff.

### 3. Abstract
- A concise 250-word overview of the desktop quiz portal, its offline SQLite architecture, modular design, and educational assessment utility.

### 4. Introduction
- 1.1 Problem Statement: Shortcomings of pen-and-paper or bloated online quiz software.
- 1.2 Proposed System: Lightweight, offline-capable, responsive Python desktop tool with instant analytics.
- 1.3 Scope of the Project: Academic testing in programming, algorithmic problem-solving, and AI concepts.

### 5. System Requirements Specification (SRS)
- **Software Requirements**: Windows 10/11, Python 3.8+, Tkinter GUI library, SQLite 3.
- **Hardware Requirements**: Intel/AMD x86-64 Dual-Core CPU, 4 GB RAM, 100 MB free storage.

### 6. System Architecture & Design
- 6.1 Architectural Pattern: Model-View-Controller (MVC) paradigm implemented via Python modules (`ui.py` for View, `database.py` for Model, `main.py` for Controller).
- 6.2 Database Schema: Entity-Relationship diagram for `questions` and `quiz_attempts`.
- 6.3 State Flow & Screen Navigation Statechart.

### 7. Implementation Details
- 7.1 Graphical User Interface design using Tkinter and TTK themes.
- 7.2 Non-blocking countdown timer implementation via `root.after()`.
- 7.3 Answer selection, persistence, and state tracking mechanisms.
- 7.4 Scoring and letter grade categorization logic.

### 8. Testing & Validation
- Unit testing methodology using Python's `unittest` framework.
- Test cases covering database integrity, timer tick accuracy, scoring edge cases, and empty input handling.

### 9. Results & Discussion
- Screen captures and functional evaluation of each screen.
- Analysis of candidate feedback during mock testing.

### 10. Conclusion & Future Enhancements
- Summary of project achievements.
- Future roadmap: Exporting scorecards to PDF, audio feedback/sound effects, network-synchronized multiplayer mode, and adaptive question difficulty.

### 11. References
- Official Python Documentation: `docs.python.org`
- Tkinter Reference Manual & SQLite 3 Specification.
- Textbooks: *Python Crash Course* by Eric Matthes; *Artificial Intelligence: A Modern Approach* by Russell & Norvig.

---

## 💡 Viva Questions and Answers (20 Questions for Examination)

**Q1: What is the overall architecture of this application?**  
*Answer:* The application follows the Model-View-Controller (MVC) design pattern. `database.py` and `quiz_data.py` serve as the Model (data persistence and schemas), `ui.py` acts as the View (user interface and presentation), and `main.py` functions as the Controller (routing and state management).

**Q2: Why did you choose Tkinter over web frameworks like Django or Flask for this project?**  
*Answer:* Tkinter is Python's standard desktop GUI toolkit. It runs natively on the client machine without requiring web server setup, network ports, browser compatibility handling, or active internet connectivity, making it ideal for offline college laboratories.

**Q3: How does the countdown timer work without freezing the GUI?**  
*Answer:* Instead of using Python's blocking `time.sleep()`, the timer uses Tkinter's event-driven `after(1000, callback)` method. This schedules the next tick asynchronously on the main GUI event loop, keeping all buttons and animations responsive.

**Q4: How are previous quiz attempts stored persistently?**  
*Answer:* We use an embedded SQLite database (`quiz_portal.db`). The `quiz_attempts` table stores the candidate name, subject category, difficulty level, raw score, total questions, percentage, letter grade, time taken, and timestamp.

**Q5: What happens if a user submits the quiz with unanswered questions?**  
*Answer:* The system dynamically counts questions where `user_answers[idx] is None` and triggers a confirmation modal warning the student about the exact number of unanswered questions, preventing accidental submissions.

**Q6: What is SQLite and why is it suitable for this college project?**  
*Answer:* SQLite is a serverless, self-contained, zero-configuration relational database engine embedded directly into Python's standard library. It stores all tables in a single cross-platform file, eliminating external database server dependencies.

**Q7: How do you prevent SQL Injection in your database module?**  
*Answer:* We use parameterized SQL queries (e.g., `cursor.execute("SELECT ... WHERE category = ?", (cat,))`). User inputs are passed as parameters rather than string formatting, allowing the database engine to safely escape all values.

**Q8: Can a student change their answer before final submission?**  
*Answer:* Yes. The application maintains an in-memory dictionary `user_answers` mapping question indices to selected option indices. Selecting another option updates this mapping and re-renders the visual state instantly.

**Q9: How is the Question Palette implemented?**  
*Answer:* A horizontal strip of numbered buttons corresponding to questions 1 through $N$ is generated dynamically. Each button is color-coded: Green for answered, Cyan for the active question, and Dark Slate for unanswered. Clicking any button invokes `jump_to_question()`.

**Q10: What algorithm is used to select questions for each quiz session?**  
*Answer:* The database executes `SELECT * FROM questions WHERE category = ? AND difficulty = ? ORDER BY RANDOM() LIMIT ?`. This randomizes the questions fetched so candidates receive a varied set on every attempt.

**Q11: How do you calculate the academic grade for each quiz?**  
*Answer:* The percentage is calculated as `(score / total_questions) * 100`. Based on standard college grading scales, $\ge 90\%$ receives $A^+$ (Outstanding), $\ge 80\%$ gets $A$ (Excellent), down to $< 40\%$ which receives $F$ (Needs Improvement).

**Q12: How are detailed question explanations displayed?**  
*Answer:* On the Results Screen, clicking "Review Answers & Explanations" opens a scrollable `ReviewDialog` window containing all questions, student choices, the correct options, and the educational explanations stored in the database.

**Q13: What is the purpose of the `ttk.Treeview` widget in `ui.py`?**  
*Answer:* `ttk.Treeview` is used in the History Screen to display tabular data with columns for Attempt ID, Student Name, Category, Difficulty, Score, Percentage, Grade, and Timestamp.

**Q14: How does the application handle window resizing on different screens?**  
*Answer:* We use Tkinter's `pack(fill="both", expand=True)` and `grid` geometry managers with column/row weight configurations. This enables cards and text boxes to expand or contract responsively.

**Q15: What is the purpose of `requirements.txt` if only standard libraries are used?**  
*Answer:* It serves as standardized documentation for external evaluators and examiners, stating Python version compatibility ($\ge 3.8$) and explicitly noting that zero third-party dependencies are required.

**Q16: How do you ensure the database tables are created automatically on a fresh installation?**  
*Answer:* `database.init_db()` runs `CREATE TABLE IF NOT EXISTS` statements during application startup. If the question table is empty, it automatically seeds all 75 questions from `quiz_data.py`.

**Q17: What happens when the countdown timer reaches zero?**  
*Answer:* The `tick_timer()` callback detects `timer_seconds_left <= 0`, halts the recurring timer via `stop_countdown_timer()`, displays an alert informing the student that time has expired, and automatically calls `finalize_and_submit()`.

**Q18: What is the role of `test_quiz_app.py` in your project?**  
*Answer:* It contains automated unit tests using Python's `unittest` module to verify data integrity, database operations, scoring algorithms, and UI screen transitions, adhering to industry software quality standards.

**Q19: How does the application clean up background timers if the user closes the window mid-quiz?**  
*Answer:* The master window binds the `WM_DELETE_WINDOW` protocol to an `on_exit()` handler. It asks for exit confirmation and cancels pending `root.after()` timer calls to avoid memory leaks or orphan background loops.

**Q20: Mention two potential future enhancements for this project.**  
*Answer:* 1) Implementing an automated PDF report generator using `ReportLab` to print student score certificates. 2) Adding user authentication with password hashing and role-based permissions (Student vs. Teacher/Admin).

---

## 🎤 Presentation Script (For College Project Viva / Demo)

> **Duration:** 3 - 5 Minutes  
> **Audience:** External Examiner, Project Guide, and Classmates

### 1. Introduction (30 Seconds)
*"Good morning, respected examiners and faculty members. Today, I am proud to present **BrainQuest**, a modern, responsive Technical Quiz and Assessment Portal developed for our B.Tech 2nd-year CSE (AIML) coursework.*

*In computer science education, fast and reliable self-assessment tools are critical. Many existing platforms either require an active internet connection or are overly simplistic command-line scripts. We built BrainQuest to provide a full-featured, visually appealing desktop assessment system using pure Python, Tkinter, and SQLite."*

### 2. Technologies & Architecture (45 Seconds)
*"The application is built on a clean 3-tier modular architecture:
- **Presentation Layer (`ui.py`):** Uses Tkinter and ttk with a custom modern Dark Slate and Indigo aesthetic, card-based components, and smooth hover interactions.
- **Business Logic Layer (`main.py`):** Coordinates screen transitions, scoring, and non-blocking asynchronous countdown timers.
- **Data Layer (`database.py` and `quiz_data.py`):** Uses SQLite to manage questions and store complete attempt histories persistently.
Crucially, the entire portal relies exclusively on Python's standard library, ensuring zero dependency conflicts and complete offline functionality."*

### 3. Live Demonstration & Workflow (2 Minutes)
*"Allow me to demonstrate the user journey:
1. **Welcome Screen:** We begin by entering the student's name, for example, 'Mansi Sharma'. Here we can view featured topics or check previous attempt histories.
2. **Dashboard:** The candidate selects their preferred technical domain—such as 'Artificial Intelligence and Machine Learning'—chooses a difficulty level, and sets the question count.
3. **Active Quiz:** Upon launching, a countdown timer starts at the top right. As you can see, questions are rendered with clear multiple-choice options. Notice the **Question Palette** at the bottom: as I answer Question 1, its indicator turns emerald green. I can navigate back and forth, change my answer freely, or jump straight to Question 5.
4. **Auto-Submit & Confirmation:** If I attempt to submit early with unanswered questions, the portal warns me. When submitted, our scoring engine calculates accuracy, assigns a letter grade, and records the session in SQLite.
5. **Results & Review:** The student receives an instant report card with score, accuracy grade, and time taken. Clicking 'Review Answers' opens a detailed breakdown where every question is paired with an in-depth technical explanation."*

### 4. Conclusion & Takeaway (30 Seconds)
*"To verify the robustness of our software, we have implemented an automated test suite with Python's `unittest` framework, validating database persistence, timer logic, and scoring accuracy. BrainQuest exemplifies how core Python concepts—such as OOP, event-driven GUI programming, and database design—combine into a real-world academic tool. Thank you, and I am now ready for questions."*
