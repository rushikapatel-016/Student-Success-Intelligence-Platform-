import sqlite3
from database.db_connection import create_connection


class Marks:
    def __init__(self, student_id, subject_name, score):
        self.student_id = student_id
        self.subject_name = subject_name
        self.score = score

    def save_to_database(self):
        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO marks (student_id, subject_name, score)
                VALUES (?, ?, ?)
            """, (self.student_id, self.subject_name, self.score))

            connection.commit()
            print(f"Mark for subject '{self.subject_name}' saved successfully for student ID {self.student_id}.")

        except sqlite3.IntegrityError:
            print("Error: Could not save mark — check that the student ID exists.")

        finally:
            connection.close()

    @staticmethod
    def get_marks_by_student(student_id):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT subject_name, score FROM marks WHERE student_id = ?
        """, (student_id,))

        results = cursor.fetchall()
        connection.close()
        return results


if __name__ == "__main__":
    marks_list = Marks.get_marks_by_student(1)
    for subject, score in marks_list:
        print(f"{subject}: {score}")