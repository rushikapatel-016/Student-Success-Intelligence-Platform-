# 🎉 Successfully pushed to GitHub!

```
[main 7741444] Add Faculty Dashboard; fix foreign key enforcement and subject name validation
 3 files changed, 141 insertions(+), 34 deletions(-)
 create mode 100644 dashboards/faculty_dashboard.py
```

Milestone 9 is fully saved. Both your Student Dashboard and Faculty Dashboard are now live, tested, and working.

---

# Milestone 9 Documentation

Milestone 9: Faculty Dashboard

Objective
Build the administrative counterpart to the Student Dashboard (Milestone 8) — a menu-driven Faculty Dashboard allowing faculty to add students, record marks, view all students, update or delete student records, view class-wide analytics, and identify students needing academic support, all from a single unified interface.

Why This Milestone Matters
With both the Student Dashboard and Faculty Dashboard complete, the platform reaches genuine feature-completeness for its core mission: students can check their own progress, and faculty can manage records and identify who needs help, directly fulfilling the "Faculty Dashboard" feature block from the original project plan.

Concepts Covered
- Reusing existing CRUD methods (Student, Marks) in an administrative context
- Reusing analytics functions from a faculty perspective
- Input validation against a fixed, known list of acceptable values
- SQLite foreign key enforcement, and why it must be explicitly enabled
- Diagnosing a data integrity bug using direct verification rather than assumption
- Consolidating multiple existing components into a final, polished interface

Folder Structure
A new file, faculty_dashboard.py, was added inside the existing dashboards/ folder alongside student_dashboard.py from Milestone 8.

Bug Discovery: Foreign Key Enforcement Was Never Active

While testing add_marks() with a deliberately invalid student ID (90, which did not exist), the system reported "saved successfully" rather than rejecting the invalid reference. This was verified directly:

python -c "...cursor.execute('SELECT * FROM students WHERE student_id = 90'); print(cursor.fetchall())..."
Output: []

Confirming student ID 90 did not exist, yet a mark record referencing it had been created — an orphaned record violating the foreign key relationship declared back in Milestone 3.

Root cause: SQLite disables foreign key constraint enforcement by default on every connection, unless explicitly enabled via a PRAGMA statement. This had never been added, meaning the FOREIGN KEY (student_id) REFERENCES students (student_id) clause in the marks table definition had been declared but never actually enforced since Milestone 3.

Fix applied to database/db_connection.py:

def create_connection():
    connection = sqlite3.connect("data/student_success.db")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

Since every part of the application obtains its connection through this single function, this one change enforces the constraint everywhere at once.

Corresponding update to models/marks.py, to handle the resulting error gracefully rather than crashing:

except sqlite3.IntegrityError:
    print(f"Error: Student ID {self.student_id} does not exist. Mark not saved.")

Verification: Re-attempting to add a mark for a non-existent student ID correctly produced "Error: Student ID [id] does not exist. Mark not saved." A subsequent test using a real, valid student ID correctly succeeded, confirming the fix blocked invalid references while preserving normal functionality.

Second Data Quality Issue: Subject Name Fragmentation

While reviewing class analytics after testing, a subject named "mathematics" appeared as a separate row from the existing "Math" category, with its own distinct average. This mirrored the department-name fragmentation issue discovered in Milestone 7, but in the marks table's subject_name column, which had no constraint limiting it to a fixed set of values.

The existing bad data was corrected with a one-time script:

cursor.execute("UPDATE marks SET subject_name = 'Math' WHERE subject_name = 'mathematics'")

To prevent recurrence, add_marks() was updated to validate against a fixed list before any database interaction:

VALID_SUBJECTS = ["Math", "Science", "English"]

def add_marks():
    ...
    subject_name = input("Enter subject name: ")

    if subject_name not in VALID_SUBJECTS:
        print(f"Error: '{subject_name}' is not a recognized subject.")
        return
    ...

This is an exact-match, case-sensitive check; a documented limitation is that it does not normalize casing (e.g., "math" in lowercase would still be rejected) or draw its valid values dynamically from the subjects table — a reasonable future improvement, though the current fix directly resolves the category-fragmentation problem encountered.

Core Feature Implementation

def add_student(): — reuses the Student class directly, mirroring the equivalent function in app.py from Milestone 4.

def add_marks(): — validates the subject name, then converts the input score from text to a number using float(), catching ValueError if the input is not a valid number, consistent with the exception-handling approach established in Milestone 4.

def view_all_students(): — reuses Student.get_all_students(), formatted identically to app.py.

def update_student() and def delete_student(): — reuse the existing, previously-fixed CRUD methods from Milestone 4 (which already correctly report "no student found" for invalid IDs via rowcount checking).

def view_class_analytics(): — reuses class_average(), average_score_per_subject(), and student_rankings() from Milestone 5, presented together as a single faculty-facing report.

def view_weak_performers(): — reuses identify_weak_performers() from Milestone 5, directly fulfilling the "Identify Weak Students" feature from the original project plan.

Menu System

def show_faculty_menu(): and def main(): follow the same while True / break menu-loop pattern established in app.py (Milestone 4) and student_dashboard.py (Milestone 8), offering eight options: Add Student, Add Marks, View All Students, Update Student, Delete Student, View Class Analytics, View Students Needing Attention, and Exit.

Verified end-to-end test: Successfully navigated View All Students, Add Student, View Class Analytics (confirmed clean three-subject breakdown post-fix), View Students Needing Attention (correctly flagged kenvi and karan patel), and Exit, with the menu correctly redisplaying after each action.

Complete File: dashboards/faculty_dashboard.py

from models.student import Student
from models.marks import Marks
from analytics.student_analytics import load_marks_dataframe, class_average, average_score_per_subject, student_rankings, identify_weak_performers


VALID_SUBJECTS = ["Math", "Science", "English"]


def add_student():
    print("\n--- Add New Student ---")
    name = input("Enter name: ")
    roll_number = input("Enter roll number: ")
    email = input("Enter email: ")
    department = input("Enter department: ")

    student = Student(name, roll_number, email, department)
    student.save_to_database()


def add_marks():
    print("\n--- Add Marks ---")
    student_id = input("Enter student ID: ")

    print(f"Valid subjects: {', '.join(VALID_SUBJECTS)}")
    subject_name = input("Enter subject name: ")

    if subject_name not in VALID_SUBJECTS:
        print(f"Error: '{subject_name}' is not a recognized subject.")
        return

    score = input("Enter score: ")

    try:
        score = float(score)
    except ValueError:
        print("Error: Score must be a number.")
        return

    mark = Marks(student_id, subject_name, score)
    mark.save_to_database()


def view_all_students():
    students = Student.get_all_students()
    if not students:
        print("No students found.")
        return

    print("\n--- All Students ---")
    for student in students:
        print(f"ID: {student[0]} | Name: {student[1]} | Roll: {student[2]} | Email: {student[3]} | Dept: {student[4]}")


def update_student():
    print("\n--- Update Student ---")
    student_id = input("Enter student ID to update: ")
    new_email = input("Enter new email (leave blank to skip): ")
    new_department = input("Enter new department (leave blank to skip): ")

    Student.update_student(
        student_id,
        email=new_email if new_email else None,
        department=new_department if new_department else None
    )


def delete_student():
    print("\n--- Delete Student ---")
    student_id = input("Enter student ID to delete: ")
    Student.delete_student(student_id)


def view_class_analytics():
    df = load_marks_dataframe()

    print("\n--- Class Analytics ---")
    print(f"Class average score: {class_average(df):.2f}")

    print("\nAverage score per subject:")
    print(average_score_per_subject(df))

    print("\nStudent rankings:")
    print(student_rankings(df))


def view_weak_performers():
    df = load_marks_dataframe()
    weak_students = identify_weak_performers(df)

    print("\n--- Students Needing Attention (average below 60) ---")
    if weak_students.empty:
        print("No students currently below the threshold.")
    else:
        print(weak_students)


def show_faculty_menu():
    print("\n===== Faculty Dashboard =====")
    print("1. Add Student")
    print("2. Add Marks")
    print("3. View All Students")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. View Class Analytics")
    print("7. View Students Needing Attention")
    print("8. Exit")


def main():
    while True:
        show_faculty_menu()
        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_marks()
        elif choice == "3":
            view_all_students()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            view_class_analytics()
        elif choice == "7":
            view_weak_performers()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()

Version Control

git add .
git commit -m "Add Faculty Dashboard; fix foreign key enforcement and subject name validation"
git push

git status confirmed dashboards/faculty_dashboard.py as new and database/db_connection.py plus models/marks.py as modified, with .gitignore continuing to correctly exclude venv/, __pycache__/, and the live database file. Temporary diagnostic and fix scripts (check_student.py, fix_subject_name.py) were deleted before committing, consistent with the pattern established for one-time utility scripts in earlier milestones.

Outcomes
The platform gained a complete, feature-rich Faculty Dashboard, reusing the majority of its logic from previously-built components rather than duplicating code — a direct payoff of the layered architecture established since Milestone 1. This milestone also surfaced and fixed a significant, previously-undetected data integrity issue (disabled foreign key enforcement) that had existed silently since Milestone 3, alongside a second recurring category-fragmentation pattern (subject names) similar to one previously encountered with department names in Milestone 7 — reinforcing that free-text data entry consistently requires either validation or normalization to remain reliable over time.

Status: Complete. Full Faculty Dashboard operational and verified end-to-end via manual testing, both the Student and Faculty Dashboards now complete, all changes committed and pushed to the public repository.
