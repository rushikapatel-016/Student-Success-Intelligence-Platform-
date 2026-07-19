import pandas as pd
from database.db_connection import create_connection


def load_marks_dataframe():
    connection = create_connection()

    query = """
        SELECT s.student_id, s.name, m.subject_name, m.score
        FROM students s
        JOIN marks m ON s.student_id = m.student_id
    """

    df = pd.read_sql_query(query, connection)
    connection.close()

    return df


def class_average(df):
    return df["score"].mean()


def highest_scoring_record(df):
    return df.loc[df["score"].idxmax()]


def lowest_scoring_record(df):
    return df.loc[df["score"].idxmin()]


def average_score_per_subject(df):
    return df.groupby("subject_name")["score"].mean()


def student_rankings(df):
    averages = df.groupby(["student_id", "name"])["score"].mean()
    ranked = averages.sort_values(ascending=False)
    return ranked


def identify_weak_performers(df, threshold=60):
    averages = df.groupby(["student_id", "name"])["score"].mean()
    weak_students = averages[averages < threshold]
    return weak_students


if __name__ == "__main__":
    df = load_marks_dataframe()

    print("Full dataset:")
    print(df)

    print(f"\nClass average score: {class_average(df):.2f}")

    print("\nHighest scoring record:")
    print(highest_scoring_record(df))

    print("\nLowest scoring record:")
    print(lowest_scoring_record(df))

    print("\nAverage score per subject:")
    print(average_score_per_subject(df))

    subject_averages = average_score_per_subject(df)
    print(f"\nHighest scoring subject: {subject_averages.idxmax()} ({subject_averages.max():.2f})")
    print(f"Lowest scoring subject: {subject_averages.idxmin()} ({subject_averages.min():.2f})")

    print("\nStudent rankings (by average score, highest to lowest):")
    print(student_rankings(df))

    print("\nStudents needing attention (average below 60):")
    weak_performers = identify_weak_performers(df)
    if weak_performers.empty:
        print("No students currently below the threshold.")
    else:
        print(weak_performers)