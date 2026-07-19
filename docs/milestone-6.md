Milestone 6: Mathematics with NumPy

Objective
Introduce NumPy to add statistical depth beyond the simple averages calculated in Milestone 5 — standard deviation, variance, correlation between subjects, a standardized GPA calculation, and a custom Performance Index combining average performance with consistency.

Why This Milestone Matters
Averages alone can be misleading. Two students could share the same average score but differ significantly in consistency — one might score close to their average every time, another might swing wildly between very high and very low results. Standard deviation and variance quantify this spread. Correlation reveals whether two variables move together, such as whether strong Math performance tends to predict strong Science performance. GPA translates raw scores into a standardized, widely-understood scale.

Concepts Covered
- NumPy arrays and conversion from Pandas Series via .to_numpy()
- Standard deviation and variance, and the mathematical relationship between them
- Correlation coefficients and their interpretation
- DataFrame reshaping using .pivot()
- .apply() for running a custom function across every value in a Series
- Weighted/standardized scoring (GPA conversion)
- Designing a custom combined metric (Performance Index)

File: analytics/statistics_analysis.py

import numpy as np
from analytics.student_analytics import load_marks_dataframe


def score_standard_deviation(df):
    scores = df["score"].to_numpy()
    return np.std(scores)


def score_variance(df):
    scores = df["score"].to_numpy()
    return np.var(scores)

Explanation: pandas Series are converted to NumPy arrays via .to_numpy() for direct use of NumPy's statistical functions, even though Pandas exposes equivalent methods internally built on NumPy — done here explicitly for learning purposes, since NumPy underlies the broader Python data and machine learning ecosystem. np.std() calculates standard deviation, a measure of how spread scores are around the mean; np.var() calculates variance, which is mathematically the square of the standard deviation. Variance is more useful in further mathematical calculations, while standard deviation is more intuitively interpretable since it shares the same units as the original data.

Verified output:
Standard deviation of all scores: 17.29
Variance of all scores: 299.03
(Confirmed 17.29² ≈ 299.03, verifying the mathematical relationship directly against real data.)

Correlation

def subject_correlation(df, subject_a, subject_b):
    pivot = df.pivot(index="student_id", columns="subject_name", values="score")
    correlation_matrix = np.corrcoef(pivot[subject_a], pivot[subject_b])
    return correlation_matrix[0, 1]

Explanation: df.pivot() reshapes the DataFrame from "long" format (one row per student-subject-score combination) into "wide" format (one row per student, with separate columns per subject) — necessary because correlation requires two aligned lists of numbers per student. np.corrcoef() computes a full correlation matrix comparing every pair among its inputs; correlation_matrix[0, 1] extracts the specific value representing the relationship between the two chosen subjects, rather than each subject's meaningless self-correlation of 1.0. Correlation values range from -1 (perfect negative relationship) through 0 (no relationship) to +1 (perfect positive relationship).

Verified output:
Correlation between Math and Science: 0.98

Interpretation note: A correlation this close to +1 indicates students who perform well in Math also strongly tend to perform well in Science in this dataset. Given the small sample size (7 students) and the deliberately consistent strong/weak/average student profiles used for testing, this result should be interpreted cautiously rather than treated as a statistically robust real-world finding — though the calculation methodology itself is correct and would scale appropriately to a larger, more organic dataset.

GPA Calculation

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

Explanation: score_to_grade_point() maps raw percentage-style scores onto a standard 4.0 grading scale (90+ = 4.0, 80-89 = 3.0, 70-79 = 2.0, 60-69 = 1.0, below 60 = 0.0), mirroring common institutional grading conventions. calculate_gpa() filters the DataFrame to a single student's rows using boolean indexing, then uses .apply() to run the grade-point conversion function across every individual score, before averaging the resulting grade points into a single GPA value.

Verified output (GPA per student):
Rushika: 3.00, Priya: 3.67, kenvi: 0.33, Aarav Sharma: 1.67, diya patel: 3.33, karan patel: 0.00, sneha patel: 2.00

These results align closely with the raw-score rankings established in Milestone 5, with karan patel's 0.00 GPA reflecting that none of his individual scores reached the 60-point threshold required for any grade points.

Performance Index

def performance_index(df, student_id):
    student_scores = df[df["student_id"] == student_id]["score"].to_numpy()

    avg_score = np.mean(student_scores)
    consistency = np.std(student_scores)

    index = avg_score - consistency
    return index

Explanation: This custom metric combines a student's average score with a penalty proportional to their own individual standard deviation, rewarding consistent performance over high-but-erratic performance. Two students with identical averages but different consistency levels will receive different Performance Index scores — the more consistent student scoring higher, since less is subtracted from their average.

Verified output (Performance Index per student):
Rushika: 79.55, Priya: 88.80, kenvi: 46.21, Aarav Sharma: 66.06, diya patel: 85.55, karan patel: 37.74, sneha patel: 69.68

As expected, every student's Performance Index falls below their raw average score, with the size of the gap reflecting each student's individual score variability across subjects.

Complete File: analytics/statistics_analysis.py

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

Version Control

git add .
git commit -m "Add NumPy statistical analysis: standard deviation, variance, correlation, GPA, and performance index"
git push

git status confirmed analytics/statistics_analysis.py as a single new file, with .gitignore continuing to correctly exclude venv/, __pycache__/, and the live database file.

Outcomes
The platform gained deeper statistical capability beyond simple averaging, introducing measures of data spread (standard deviation, variance), relationships between variables (correlation), standardized scoring (GPA), and a custom-designed composite metric (Performance Index) that rewards consistency alongside raw performance. This milestone also reinforced responsible interpretation of statistical results, explicitly noting the limitations of drawing strong conclusions from a small, deliberately-constructed test dataset.

