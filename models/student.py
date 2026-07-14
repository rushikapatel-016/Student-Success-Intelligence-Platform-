import sqlite3
from database.db_connection import create_connection


class Student:
    def __init__(self, name, roll_number, email, department):
        self.name = name
        self.roll_number = roll_number
        self.email = email
        self.department = department

    def save_to_database(self):
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


if __name__ == "__main__":
    student1 = Student("Rushika", "101", "rushika@example.com", "Computer Science")
    student1.save_to_database()