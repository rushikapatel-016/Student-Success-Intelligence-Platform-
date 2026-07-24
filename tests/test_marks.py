import unittest
import os
import sqlite3
from models.student import Student
from models.marks import Marks
import models.student as student_module
import models.marks as marks_module


TEST_DB = "data/test_marks_success.db"


def test_connection():
    conn = sqlite3.connect(TEST_DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


class TestMarks(unittest.TestCase):

    def setUp(self):
        student_module.create_connection = test_connection
        marks_module.create_connection = test_connection

        conn = sqlite3.connect(TEST_DB)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_number TEXT NOT NULL UNIQUE,
                email TEXT,
                department TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS marks (
                mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_name TEXT NOT NULL,
                score REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (student_id)
            )
        """)
        conn.commit()
        conn.close()

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_valid_mark_saves_successfully(self):
        student = Student("Test Student", "M001", "test@example.com", "Testing")
        student.save_to_database()

        mark = Marks(1, "Math", 90)
        mark.save_to_database()

        results = Marks.get_marks_by_student(1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], ("Math", 90))

    def test_mark_for_nonexistent_student_is_rejected(self):
        mark = Marks(999, "Math", 90)
        mark.save_to_database()

        results = Marks.get_marks_by_student(999)
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()