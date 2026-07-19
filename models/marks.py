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
    marks_data = [
        (1, "Math", 85.5),
        (1, "Science", 90),
        (1, "English", 78),

        (3, "Math", 92),
        (3, "Science", 88),
        (3, "English", 95),

        (4, "Math", 45),
        (4, "Science", 52),
        (4, "English", 60),

        (5, "Math", 70),
        (5, "Science", 65),
        (5, "English", 72),

        (6, "Math", 88),
        (6, "Science", 91),
        (6, "English", 85),

        (7, "Math", 38),
        (7, "Science", 42),
        (7, "English", 55),

        (8, "Math", 76),
        (8, "Science", 80),
        (8, "English", 68),
    ]

    for student_id, subject, score in marks_data:
        mark = Marks(student_id, subject, score)
        mark.save_to_database()