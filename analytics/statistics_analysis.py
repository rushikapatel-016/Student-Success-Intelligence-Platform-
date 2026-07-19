import numpy as np
from analytics.student_analytics import load_marks_dataframe


def score_standard_deviation(df):
    scores = df["score"].to_numpy()
    return np.std(scores)


def score_variance(df):
    scores = df["score"].to_numpy()
    return np.var(scores)


def subject_correlation(df, subject_a, subject_b):
    pivot = df.pivot(index="student_id", columns="subject_name", values="score")
    correlation_matrix = np.corrcoef(pivot[subject_a], pivot[subject_b])
    return correlation_matrix[0, 1]


def score_to_grade_point(score):
    if score >= 90:
        return 4.0
    elif score >= 80:
        return 3.0
    elif score >= 70:
        return 2.0
    elif score >= 60:
        return 1.0
    else:
        return 0.0


def calculate_gpa(df, student_id):
    student_scores = df[df["student_id"] == student_id]["score"]
    grade_points = student_scores.apply(score_to_grade_point)
    return grade_points.mean()


def performance_index(df, student_id):
    student_scores = df[df["student_id"] == student_id]["score"].to_numpy()

    avg_score = np.mean(student_scores)
    consistency = np.std(student_scores)

    index = avg_score - consistency
    return index


if __name__ == "__main__":
    df = load_marks_dataframe()

    print(f"Standard deviation of all scores: {score_standard_deviation(df):.2f}")
    print(f"Variance of all scores: {score_variance(df):.2f}")

    correlation = subject_correlation(df, "Math", "Science")
    print(f"\nCorrelation between Math and Science: {correlation:.2f}")

    print("\nGPA for each student:")
    for student_id in df["student_id"].unique():
        name = df[df["student_id"] == student_id]["name"].iloc[0]
        gpa = calculate_gpa(df, student_id)
        print(f"{name}: GPA {gpa:.2f}")

    print("\nPerformance Index for each student:")
    for student_id in df["student_id"].unique():
        name = df[df["student_id"] == student_id]["name"].iloc[0]
        index = performance_index(df, student_id)
        print(f"{name}: Performance Index {index:.2f}")