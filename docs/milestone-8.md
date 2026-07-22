# 🎉 Successfully pushed to GitHub!

```
[main 578b185] Add Student Dashboard with login, profile, marks, GPA, chart, and progress report
 2 files changed, 126 insertions(+)
 create mode 100644 dashboards/student_dashboard.py
```

Milestone 8 is fully saved and live on your repository. (That last "nothing to commit" and "Everything up-to-date" just confirmed the push already succeeded — no issue there, just running the commands again on an already-clean state.)

---

# Milestone 8 Documentation

Milestone 8: Student Dashboard

Objective
Assemble the platform's existing capabilities — database access, marks retrieval, GPA calculation, and personalized visualization — into a cohesive, student-facing feature: a menu-driven Student Dashboard allowing an individual student to log in by roll number and view their own profile, marks, GPA, performance chart, and an automated progress report.

Why This Milestone Matters
Every feature built through Milestones 2-7 was inherently admin or faculty-facing — tools for managing and analyzing the whole class. This milestone shifts perspective to the student's own point of view, directly fulfilling the "Student Dashboard" feature block from the original project plan (Login, View Profile, View Marks, GPA, Progress Report, Performance Charts).

Concepts Covered
- Designing a feature around a specific user role rather than an administrative perspective
- Reusing existing models, analytics, and visualization code across a new context
- A simple identity-lookup login flow (by roll number, without password authentication)
- List comprehensions combined with tuple unpacking
- Rule-based automated feedback generation
- A second, independent menu-loop pattern alongside the existing app.py CLI

Design Note on Authentication
Login in this milestone means entering a roll number, which the system uses to look up and display only that student's own data. No password or credential verification exists yet. This is a deliberate, documented scope decision appropriate to this stage of the project; genuine authentication (passwords, sessions) would be a reasonable addition in a future security-focused milestone.

Folder Structure
A new folder, dashboards/, was introduced containing student_dashboard.py, keeping this user-facing feature separate from the underlying models, analytics, and visualization layers it depends on.

Step 1: Roll Number Lookup

Added to models/student.py:

    @staticmethod
    def get_student_by_roll_number(roll_number):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT student_id, name, roll_number, email, department
            FROM students WHERE roll_number = ?
        """, (roll_number,))
        result = cursor.fetchone()

        connection.close()
        return result

Explanation: Nearly identical in structure to the existing get_student_by_id(), but filters by roll_number instead. Since roll_number carries a UNIQUE constraint (established in Milestone 2), at most one row can ever match, making fetchone() the correct choice — consistent with how get_student_by_id() was implemented in Milestone 4.

Step 2: Login Flow

def login():
    roll_number = input("Enter your roll number to log in: ")
    student = Student.get_student_by_roll_number(roll_number)

    if student is None:
        print("No student found with that roll number.")
        return None

    print(f"\nWelcome, {student[1]}!")
    return student

Explanation: Prompts for a roll number and looks up the matching student. If none exists, fetchone() returns None, and a friendly message is shown rather than proceeding further. On success, the full student tuple is returned so subsequent dashboard functions can reuse it without repeating the lookup.

Verified behavior: An incorrect roll number correctly returned "No student found with that roll number." A correct roll number (101) correctly returned "Welcome, Rushika!"

Step 3: View Profile

def view_profile(student):
    print("\n--- Your Profile ---")
    print(f"Name: {student[1]}")
    print(f"Roll Number: {student[2]}")
    print(f"Email: {student[3]}")
    print(f"Department: {student[4]}")

Explanation: Displays each field directly from the already-retrieved student tuple, avoiding a redundant database query since the full record was already fetched during login.

Step 4: View Marks and GPA

def view_marks_and_gpa(student):
    student_id = student[0]
    marks = Marks.get_marks_by_student(student_id)

    if not marks:
        print("\nNo marks recorded yet.")
        return

    print("\n--- Your Marks ---")
    grade_points = []
    for subject, score in marks:
        gp = score_to_grade_point(score)
        grade_points.append(gp)
        print(f"{subject}: {score} (Grade Point: {gp})")

    gpa = sum(grade_points) / len(grade_points)
    print(f"\nYour GPA: {gpa:.2f}")

Explanation: Reuses Marks.get_marks_by_student() from Milestone 3 and score_to_grade_point() from Milestone 6, rather than duplicating either. Each mark is displayed alongside its converted grade point, and GPA is computed as the mean of those grade points.

Verified output for Rushika: Math 85.5 (3.0), Science 90.0 (4.0), English 78.0 (2.0), GPA 3.00 — consistent with the GPA calculated independently in Milestone 6, confirming both calculation paths agree.

Step 5: View Performance Chart

def view_performance_chart(student):
    student_id = student[0]
    plot_student_score_trend(student_id)

Explanation: Directly reuses the line-chart function built in Milestone 7, now invoked from the student's own perspective rather than an administrator selecting a student ID manually.

Step 6: Progress Report

def view_progress_report(student):
    student_id = student[0]
    marks = Marks.get_marks_by_student(student_id)

    print("\n===== Progress Report =====")
    print(f"Name: {student[1]}")
    print(f"Roll Number: {student[2]}")
    print(f"Department: {student[4]}")

    if not marks:
        print("No marks recorded yet — unable to generate a full report.")
        return

    grade_points = [score_to_grade_point(score) for subject, score in marks]
    gpa = sum(grade_points) / len(grade_points)

    print(f"\nGPA: {gpa:.2f}")

    if gpa >= 3.0:
        print("Comment: Excellent performance! Keep up the great work.")
    elif gpa >= 2.0:
        print("Comment: Good progress. Consider extra practice to push higher.")
    else:
        print("Comment: Additional academic support is recommended.")

Explanation: Combines profile details, GPA, and an automated, rule-based comment into a single readable summary. The grade_points list is built using a list comprehension combined with tuple unpacking, a more compact equivalent to an explicit for loop. The GPA-threshold comment logic offers a simple, honest example of turning a numeric result into an actionable piece of feedback — a conceptual precursor to the "suggest areas of improvement" feature planned for the later Machine Learning phase.

Verified output for Rushika: GPA 3.00, Comment: "Excellent performance! Keep up the great work."

Step 7: Menu System

def show_dashboard_menu():
    print("\n===== Student Dashboard =====")
    print("1. View Profile")
    print("2. View Marks & GPA")
    print("3. View Performance Chart")
    print("4. View Progress Report")
    print("5. Logout")


def main():
    student = login()

    if student is None:
        return

    while True:
        show_dashboard_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            view_profile(student)
        elif choice == "2":
            view_marks_and_gpa(student)
        elif choice == "3":
            view_performance_chart(student)
        elif choice == "4":
            view_progress_report(student)
        elif choice == "5":
            print("Logged out. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

Explanation: Follows the identical while True / break menu-loop pattern established in app.py during Milestone 4, applied here as a second, independent CLI flow specific to the student role. Login occurs once at the start; if it fails, the function returns immediately rather than presenting a menu to an unverified user.

Verified end-to-end test (roll number 101): Successfully navigated View Profile, View Marks & GPA, View Performance Chart (chart generated and saved), View Progress Report, and Logout, with the menu correctly redisplaying after each action until logout was selected.

Complete File: dashboards/student_dashboard.py

from models.student import Student
from models.marks import Marks
from analytics.statistics_analysis import score_to_grade_point
from visualization.charts import plot_student_score_trend


def login():
    roll_number = input("Enter your roll number to log in: ")
    student = Student.get_student_by_roll_number(roll_number)

    if student is None:
        print("No student found with that roll number.")
        return None

    print(f"\nWelcome, {student[1]}!")
    return student


def view_profile(student):
    print("\n--- Your Profile ---")
    print(f"Name: {student[1]}")
    print(f"Roll Number: {student[2]}")
    print(f"Email: {student[3]}")
    print(f"Department: {student[4]}")


def view_marks_and_gpa(student):
    student_id = student[0]
    marks = Marks.get_marks_by_student(student_id)

    if not marks:
        print("\nNo marks recorded yet.")
        return

    print("\n--- Your Marks ---")
    grade_points = []
    for subject, score in marks:
        gp = score_to_grade_point(score)
        grade_points.append(gp)
        print(f"{subject}: {score} (Grade Point: {gp})")

    gpa = sum(grade_points) / len(grade_points)
    print(f"\nYour GPA: {gpa:.2f}")


def view_performance_chart(student):
    student_id = student[0]
    plot_student_score_trend(student_id)


def view_progress_report(student):
    student_id = student[0]
    marks = Marks.get_marks_by_student(student_id)

    print("\n===== Progress Report =====")
    print(f"Name: {student[1]}")
    print(f"Roll Number: {student[2]}")
    print(f"Department: {student[4]}")

    if not marks:
        print("No marks recorded yet — unable to generate a full report.")
        return

    grade_points = [score_to_grade_point(score) for subject, score in marks]
    gpa = sum(grade_points) / len(grade_points)

    print(f"\nGPA: {gpa:.2f}")

    if gpa >= 3.0:
        print("Comment: Excellent performance! Keep up the great work.")
    elif gpa >= 2.0:
        print("Comment: Good progress. Consider extra practice to push higher.")
    else:
        print("Comment: Additional academic support is recommended.")


def show_dashboard_menu():
    print("\n===== Student Dashboard =====")
    print("1. View Profile")
    print("2. View Marks & GPA")
    print("3. View Performance Chart")
    print("4. View Progress Report")
    print("5. Logout")


def main():
    student = login()

    if student is None:
        return

    while True:
        show_dashboard_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            view_profile(student)
        elif choice == "2":
            view_marks_and_gpa(student)
        elif choice == "3":
            view_performance_chart(student)
        elif choice == "4":
            view_progress_report(student)
        elif choice == "5":
            print("Logged out. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()

Version Control

git add .
git commit -m "Add Student Dashboard with login, profile, marks, GPA, chart, and progress report"
git push

git status confirmed dashboards/ as a new directory and models/student.py as modified, with .gitignore continuing to correctly exclude venv/, __pycache__/, and the live database file.

Outcomes
The platform gained its first fully-assembled, role-specific feature — a working Student Dashboard combining database access, statistical calculation, visualization, and simple rule-based feedback into a single cohesive, menu-driven experience. This milestone demonstrated how previously-built, independent components (models, analytics, visualization) can be composed into a higher-level feature without duplicating logic, a key architectural benefit of the project's layered folder structure established from Milestone 1 onward.

