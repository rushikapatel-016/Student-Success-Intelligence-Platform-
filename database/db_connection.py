import sqlite3

def create_connection():
    connection = sqlite3.connect("data/student_success.db")
    connection.execute("PRAGMA foreign_keys = ON")
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

def create_subjects_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL UNIQUE
        )
    """)
    connection.commit()
    connection.close()

def create_marks_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_name TEXT NOT NULL,
            score REAL NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
    """)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    create_subjects_table()
    create_marks_table()
    print("Database, students table, subjects table, and marks table created successfully.")