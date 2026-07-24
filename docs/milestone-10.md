🎉 Successfully pushed to GitHub!
[main 5b3d25c] Add unit tests for Student and Marks classes covering validation, duplicates, and foreign key enforcement
 2 files changed, 142 insertions(+)
 create mode 100644 tests/test_marks.py
 create mode 100644 tests/test_student.py

Milestone 10 is fully saved and live on your repository.

Milestone 10 Documentation

Milestone 10: Testing & Validation

Objective
Introduce formal testing practices to the platform — automated unit tests using Python's built-in unittest module, alongside a documented manual testing checklist covering the CLI and both dashboards — verifying existing functionality and guarding against future regressions.

Why This Milestone Matters
Throughout this project, several real bugs were discovered through manual testing (false success messages in Milestone 4, silently disabled foreign key enforcement in Milestone 9). Automated tests catch these kinds of issues before they occur in normal use, and critically, prevent them from silently reappearing if code is changed later — a practice known as regression testing.

Concepts Covered

Python's built-in unittest module and the TestCase class
setUp() and tearDown() for isolated, repeatable test environments
Assertion methods: assertEqual, assertTrue, assertFalse, assertIsNone, assertIsNotNone
Monkey-patching for redirecting database connections during tests
Test discovery and running an entire test suite with one command
The importance of accurately mirroring production configuration within test setup

Folder Structure
A new tests/ folder was introduced, containing test_student.py and test_marks.py, matching the structure specified in the original project plan.

Part 1: Test Environment Setup

Code:
TEST_DB = "data/test_student_success.db"

class TestStudent(unittest.TestCase):

def setUp(self):
    import models.student as student_module
    student_module.create_connection = lambda: sqlite3.connect(TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("""CREATE TABLE IF NOT EXISTS students (...)""")
    conn.commit()
    conn.close()

def tearDown(self):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

Explanation: Every test class inherits from unittest.TestCase, gaining access to its built-in assertion methods. setUp() is a special method name automatically run before every individual test, used here to create a fresh, empty test database. tearDown() is automatically run after every test, deleting the test database file to guarantee each test starts from a clean state with no leftover data from previous runs.

Bug discovered and fixed: The initial approach patched database.db_connection.create_connection directly, which did not redirect models/student.py, since from database.db_connection import create_connection copies a direct reference to the function at import time — patching the original module afterward does not affect that already-copied reference. This caused early test runs to operate against the real production database rather than the intended test database, evidenced by real student names (e.g., "Rushika") and real record counts appearing in test failure output. The fix required patching create_connection specifically within the models.student module's own namespace, where the function is actually used.

Part 2: Testing the Student Class

Five tests were implemented:

def test_valid_student_saves_successfully(self):
student = Student("Test Student", "T001", "test@example.com", "Testing")
student.save_to_database()
result = Student.get_student_by_id(1)
self.assertIsNotNone(result)
self.assertEqual(result[1], "Test Student")

def test_invalid_name_is_rejected(self):
student = Student("", "T002", "test@example.com", "Testing")
self.assertFalse(student.is_valid())

def test_invalid_email_is_rejected(self):
student = Student("Test Student", "T003", "notanemail", "Testing")
self.assertFalse(student.is_valid())

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

Explanation: Each test verifies one specific, previously manually-tested behavior: successful save and retrieval, validation rejection for an empty name and a malformed email, correct handling of duplicate roll numbers (only one record should persist, since the Milestone 2 IntegrityError handling should silently reject the second), and correct None-return behavior for a non-existent ID. Test method names are required to begin with test_, the convention unittest uses to automatically discover which methods represent actual tests.

Verified output (after the connection-patching fix): All 5 tests passed, with output confirming no real production data (e.g., "Rushika") appeared anywhere in the results.

Part 3: Testing the Marks Class

Two tests were implemented:

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

Explanation: The second test directly and automatically verifies the Milestone 9 foreign key enforcement fix — attempting to save a mark referencing a student ID that was never created, then confirming zero mark records exist for that ID.

Second bug discovered, this time in the test setup itself: The initial test connection-replacement function called sqlite3.connect(TEST_DB) directly, without including PRAGMA foreign_keys = ON — meaning the test database's connections did not actually enforce foreign key constraints, despite the real application's create_connection() doing so. This caused the invalid mark to be saved successfully in the test environment, producing a false test failure that did not reflect the application's true (and previously verified, in Milestone 9) behavior. The fix replaced the bare lambda with a small named function replicating the exact PRAGMA-enabling behavior of the real create_connection():

def test_connection():
conn = sqlite3.connect(TEST_DB)
conn.execute("PRAGMA foreign_keys = ON")
return conn

This is a notable, honest lesson: test setup must accurately mirror production configuration, or tests can produce misleading results about code that is, in fact, already correct.

Verified output (after the fix): Both tests passed, with the terminal output explicitly showing "Error: Student ID 999 does not exist. Mark not saved." — confirming the foreign key protection functioned correctly within the isolated test environment.

Part 4: Running the Full Test Suite

Command:
python -m unittest discover tests

Explanation: The discover subcommand automatically locates and runs every file matching the test_*.py naming pattern within the specified folder, executing all test classes and methods across the entire tests/ directory in a single command.

Verified output: All 7 tests (5 from test_student.py, 2 from test_marks.py) passed together.

Part 5: Manual Testing Checklist

Certain behaviors — particularly those involving interactive input() prompts or Matplotlib popup windows — are more practically verified by hand than automated. The following checklist documents manual verification already performed throughout this project's development:

CLI (app.py):

Add Student with valid data succeeds
Add Student with empty name is rejected
Add Student with invalid email is rejected
View All Students displays all records correctly
View Student by ID returns the correct record for a valid ID
Update Student with a valid ID and new email succeeds
Update Student with a non-existent ID shows an accurate error, not a false success
Update Student with no fields provided shows an accurate error
Delete Student with a valid ID succeeds
Delete Student with a non-existent ID shows an accurate error
An invalid menu choice shows a friendly error rather than crashing
The Exit option cleanly terminates the program

Student Dashboard:

Login with a valid roll number succeeds
Login with an invalid roll number shows an accurate error
View Profile displays correct data
View Marks & GPA displays correct calculations
View Performance Chart generates and saves correctly
Progress Report generates an appropriate comment based on GPA
Logout cleanly exits the menu loop

Faculty Dashboard:

Add Student and Add Marks both function correctly
An invalid student ID for Add Marks is correctly rejected (foreign key fix)
An invalid subject name is correctly rejected (validation fix)
View Class Analytics displays correct aggregated data
View Students Needing Attention correctly filters by threshold
Update and Delete Student correctly reuse verified CRUD logic

Complete Files

tests/test_student.py:

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

if name == "main":
unittest.main()

tests/test_marks.py:

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

if name == "main":
unittest.main()

Version Control

git add .
git commit -m "Add unit tests for Student and Marks classes covering validation, duplicates, and foreign key enforcement"
git push

git status confirmed tests/ as a single new directory, with .gitignore continuing to correctly exclude venv/, pycache/, and both the live and test database files.

Outcomes
The platform gained a genuine automated test suite, covering both previously-manually-discovered bugs (validation, duplicate handling) and directly verifying the significant foreign key enforcement fix from Milestone 9. This milestone also surfaced two meta-level bugs within the testing infrastructure itself — an incorrectly-scoped monkey-patch and a test environment that failed to replicate a critical production setting — reinforcing that test code requires the same care and scrutiny as application code, since incorrect tests can produce misleading confidence in either direction.

Status: Complete. Full automated test suite (7 tests) passing, manual testing checklist documented across the CLI and both dashboards, all changes committed and pushed to the public repository.