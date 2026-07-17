import sqlite3
from database.db_connection import create_connection


class Student:
    def __init__(self, name, roll_number, email, department):
        self.name = name
        self.roll_number = roll_number
        self.email = email
        self.department = department

    def is_valid(self):
        if not self.name or self.name.strip() == "":
            print("Error: Name cannot be empty.")
            return False

        if not self.roll_number or self.roll_number.strip() == "":
            print("Error: Roll number cannot be empty.")
            return False

        if self.email and "@" not in self.email:
            print("Error: Email must contain '@'.")
            return False

        return True

    def save_to_database(self):
        if not self.is_valid():
            print("Student not saved due to validation errors.")
            return

        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO students (name, roll_number, email, department)
                VALUES (?, ?, ?, ?)
            """, (self.name, self.roll_number, self.email, self.department))

            connection.commit()
            print(f"Student '{self.name}' saved to database successfully.")

        except sqlite3.IntegrityError:
            print(f"Error: A student with roll number '{self.roll_number}' already exists.")

        finally:
            connection.close()

    @staticmethod
    def get_all_students():
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT student_id, name, roll_number, email, department FROM students")
        results = cursor.fetchall()

        connection.close()
        return results

    @staticmethod
    def get_student_by_id(student_id):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT student_id, name, roll_number, email, department
            FROM students WHERE student_id = ?
        """, (student_id,))
        result = cursor.fetchone()

        connection.close()
        return result

    @staticmethod
    def update_student(student_id, email=None, department=None):
        if not email and not department:
            print("Error: No update information provided.")
            return

        connection = create_connection()
        cursor = connection.cursor()

        rows_affected = 0

        if email:
            cursor.execute("UPDATE students SET email = ? WHERE student_id = ?", (email, student_id))
            rows_affected += cursor.rowcount

        if department:
            cursor.execute("UPDATE students SET department = ? WHERE student_id = ?", (department, student_id))
            rows_affected += cursor.rowcount

        connection.commit()
        connection.close()

        if rows_affected > 0:
            print(f"Student ID {student_id} updated successfully.")
        else:
            print(f"Error: No student found with ID {student_id}.")

    @staticmethod
    def delete_student(student_id):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        rows_affected = cursor.rowcount

        connection.commit()
        connection.close()

        if rows_affected > 0:
            print(f"Student ID {student_id} deleted successfully.")
        else:
            print(f"Error: No student found with ID {student_id}.")


if __name__ == "__main__":
    print("All students:")
    for student in Student.get_all_students():
        print(student)