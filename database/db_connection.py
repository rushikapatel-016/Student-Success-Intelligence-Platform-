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