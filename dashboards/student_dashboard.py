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