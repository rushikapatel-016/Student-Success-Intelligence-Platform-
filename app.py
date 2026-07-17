from models.student import Student


def show_menu():
    print("\n===== Student Success Intelligence Platform =====")
    print("1. Add Student")
    print("2. View All Students")
    print("3. View Student by ID")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")


def add_student():
    name = input("Enter name: ")
    roll_number = input("Enter roll number: ")
    email = input("Enter email: ")
    department = input("Enter department: ")

    student = Student(name, roll_number, email, department)
    student.save_to_database()


def view_all_students():
    students = Student.get_all_students()
    if not students:
        print("No students found.")
        return

    for student in students:
        print(f"ID: {student[0]} | Name: {student[1]} | Roll: {student[2]} | Email: {student[3]} | Dept: {student[4]}")


def view_student_by_id():
    student_id = input("Enter student ID: ")
    student = Student.get_student_by_id(student_id)

    if student:
        print(f"ID: {student[0]} | Name: {student[1]} | Roll: {student[2]} | Email: {student[3]} | Dept: {student[4]}")
    else:
        print("No student found with that ID.")


def update_student():
    student_id = input("Enter student ID to update: ")
    new_email = input("Enter new email (leave blank to skip): ")
    new_department = input("Enter new department (leave blank to skip): ")

    Student.update_student(
        student_id,
        email=new_email if new_email else None,
        department=new_department if new_department else None
    )


def delete_student():
    student_id = input("Enter student ID to delete: ")
    Student.delete_student(student_id)


def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            view_student_by_id()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()