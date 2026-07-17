# Milestone 2: Database Design & First Data Model

## Objective
Design and create the SQLite database, and build the platform's first Python class — introducing SQL, Python's `sqlite3` module, Object-Oriented Programming, and exception handling.

## Part 1: Database Setup

**File**: `database/db_connection.py`

```python
import sqlite3

def create_connection():
    connection = sqlite3.connect("data/student_success.db")
    return connection

def create_tables():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT NOT NULL UNIQUE,
            email TEXT,
            department TEXT
        )
    """)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    print("Database and students table created successfully.")
```

**Key concepts**: `sqlite3.connect()` creates/opens a database file. SQL `CREATE TABLE IF NOT EXISTS` builds the schema, with `PRIMARY KEY AUTOINCREMENT` for unique row identification, `NOT NULL` for required fields, and `UNIQUE` to prevent duplicate roll numbers. Verified via SQLite Viewer, confirming all 5 columns and correct constraints.

## Part 2: Object-Oriented Programming — the `Student` Class

**File**: `models/student.py`

```python
class Student:
    def __init__(self, name, roll_number, email, department):
        self.name = name
        self.roll_number = roll_number
        self.email = email
        self.department = department
```

**Key concepts**: A class is a blueprint (like a cookie cutter); an object is a specific instance built from it. `__init__` is the constructor, automatically run when a new object is created. `self` refers to the specific object being built. Verified by creating a `student1` object and printing each attribute via dot notation.

## Part 3: Connecting `Student` to the Database

**Added to `models/student.py`:**

```python
import sqlite3
from database.db_connection import create_connection

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
```

**Key concepts**:
- Parameterized queries (`?` placeholders) prevent SQL injection — values are never directly inserted into SQL text.
- `try`/`except`/`finally` handles the `UNIQUE` constraint gracefully: attempting to save a duplicate roll number is caught as `sqlite3.IntegrityError` and reported with a friendly message instead of crashing the program.
- `finally` guarantees the database connection is always closed, regardless of success or failure.

**Debugging note**: Running `python models/student.py` directly caused a `ModuleNotFoundError`, since Python only resolves imports relative to the file's own folder. Fixed by running as a module from the project root: `python -m models.student`.

**Verification**: Successfully saved a student record, confirmed via SQLite Viewer (`Rows: 1`), then intentionally re-ran the script to trigger and confirm graceful handling of the `UNIQUE constraint failed` error.

## Version Control
```bash
git add .
git commit -m "Add database setup and Student model with save functionality"
git push
```

## Status: ✅ Complete
**Skills practiced**: SQL schema design, OOP fundamentals (classes, objects, constructors), parameterized queries, exception handling, running Python as a module.
