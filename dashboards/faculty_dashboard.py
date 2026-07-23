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