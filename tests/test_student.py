import unittest
import os
import sqlite3
from models.student import Student
import models.student as student_module


TEST_DB = "data/test_student_success.db"


class TestStudent(unittest.TestCase):

    def setUp(self):
        student_module.create_connection = lambda: sqlite3.connect(TEST_DB)

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
        conn.commit()
        conn.close()

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_valid_student_saves_successfully(self):
        student = Student("Test Student", "T001", "test@example.com", "Testing")
        student.save_to_database()

        result = Student.get_student_by_id(1)
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Test Student")

    def test_invalid_name_is_rejected(self):
        student = Student("", "T002", "test@example.com", "Testing")
        is_valid = student.is_valid()

        self.assertFalse(is_valid)

    def test_invalid_email_is_rejected(self):
        student = Student("Test Student", "T003", "notanemail", "Testing")
        is_valid = student.is_valid()

        self.assertFalse(is_valid)

    def test_duplicate_roll_number_is_handled(self):
        student1 = Student("First Student", "T004", "first@example.com", "Testing")
        student1.save_to_database()

        student2 = Student("Second Student", "T004", "second@example.com", "Testing")
        student2.save_to_database()

        result = Student.get_all_students()
        self.assertEqual(len(result), 1)

    def test_get_student_by_id_returns_none_for_missing_student(self):
        result = Student.get_student_by_id(999)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()