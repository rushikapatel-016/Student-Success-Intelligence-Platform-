import matplotlib.pyplot as plt
import pandas as pd
from analytics.student_analytics import load_marks_dataframe, student_rankings
from database.db_connection import create_connection


def plot_student_rankings():
    df = load_marks_dataframe()
    rankings = student_rankings(df)

    names = [name for student_id, name in rankings.index]
    scores = rankings.values

    plt.figure(figsize=(10, 6))
    plt.bar(names, scores, color="steelblue")

    plt.title("Student Rankings by Average Score")
    plt.xlabel("Student")
    plt.ylabel("Average Score")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("screenshots/student_rankings_bar_chart.png")
    print("Bar chart saved to screenshots/student_rankings_bar_chart.png")

    plt.show()


def plot_department_distribution():
    connection = create_connection()
    query = "SELECT department FROM students"
    df = pd.read_sql_query(query, connection)
    connection.close()

    department_counts = df["department"].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(department_counts.values, labels=department_counts.index, autopct="%1.1f%%", startangle=90)

    plt.title("Student Distribution by Department")
    plt.axis("equal")

    plt.savefig("screenshots/department_distribution_pie_chart.png")
    print("Pie chart saved to screenshots/department_distribution_pie_chart.png")

    plt.show()


def plot_math_vs_science():
    df = load_marks_dataframe()
    pivot = df.pivot(index="student_id", columns="subject_name", values="score")

    plt.figure(figsize=(8, 6))
    plt.scatter(pivot["Math"], pivot["Science"], color="darkorange", s=100)

    plt.title("Math Score vs. Science Score")
    plt.xlabel("Math Score")
    plt.ylabel("Science Score")
    plt.grid(True)

    plt.savefig("screenshots/math_vs_science_scatter.png")
    print("Scatter plot saved to screenshots/math_vs_science_scatter.png")

    plt.show()


def plot_score_distribution():
    df = load_marks_dataframe()

    plt.figure(figsize=(10, 6))
    plt.hist(df["score"], bins=8, color="mediumseagreen", edgecolor="black")

    plt.title("Distribution of All Scores")
    plt.xlabel("Score")
    plt.ylabel("Frequency")

    plt.savefig("screenshots/score_distribution_histogram.png")
    print("Histogram saved to screenshots/score_distribution_histogram.png")

    plt.show()


def plot_student_score_trend(student_id):
    df = load_marks_dataframe()
    student_data = df[df["student_id"] == student_id]

    plt.figure(figsize=(8, 6))
    plt.plot(student_data["subject_name"], student_data["score"], marker="o", color="crimson", linewidth=2)

    name = student_data["name"].iloc[0]
    plt.title(f"{name}'s Scores Across Subjects")
    plt.xlabel("Subject")
    plt.ylabel("Score")
    plt.grid(True)

    plt.savefig("screenshots/student_score_trend_line_chart.png")
    print("Line chart saved to screenshots/student_score_trend_line_chart.png")

    plt.show()


if __name__ == "__main__":
    plot_student_rankings()
    plot_department_distribution()
    plot_math_vs_science()
    plot_score_distribution()
    plot_student_score_trend(1)