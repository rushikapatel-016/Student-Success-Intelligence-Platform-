Milestone 7 Documentation

Save this as docs/milestone-7.md (or paste plain into Google Docs, whichever you need).

Milestone 7: Visualizations with Matplotlib

Objective
Transform the numerical insights generated in Milestones 5 and 6 into visual charts using Matplotlib — a bar chart, pie chart, scatter plot, histogram, and line chart — making the platform's insights immediately understandable at a glance rather than requiring interpretation of printed numbers.

Why This Milestone Matters
A table of numbers requires effort to interpret. A well-designed chart communicates the same insight instantly. This milestone also produced the most visually compelling, shareable output the project has generated so far, directly supporting the portfolio and communication goals of the platform.

Concepts Covered

The core Matplotlib workflow: create a figure, plot data, add labels and title, save and/or display
Bar charts, pie charts, scatter plots, histograms, and line charts
Categorical data summarization with value_counts()
Saving figures as image files with plt.savefig()
Real-world data quality issue discovery and correction

Folder Structure
Two new folders were introduced: visualization/, containing charts.py, and screenshots/, where all generated chart images are saved as PNG files for later use in documentation or portfolio materials.

Bar Chart: Student Rankings

Code:
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
plt.show()

Explanation: The existing load_marks_dataframe() and student_rankings() functions from Milestone 5 were reused rather than duplicated. A list comprehension extracted student names from the rankings' multi-part index, discarding the accompanying student_id. plt.bar() plotted one bar per student, with plt.xticks(rotation=45) preventing long names from overlapping and plt.tight_layout() ensuring labels were not cut off at the figure's edges. The chart was saved to disk via plt.savefig() before being displayed with plt.show(), so a permanent image file exists independent of the interactive session.

Verified output: A correctly ordered, descending bar chart clearly visualizing the performance gap between top and bottom students, saved to screenshots/student_rankings_bar_chart.png.

Pie Chart: Department Distribution

Code:
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
plt.show()

Explanation: value_counts() tallies how many students fall into each unique department value. plt.pie() renders these counts as proportional slices, with autopct="%1.1f%%" automatically computing and displaying each slice's percentage, and startangle=90 beginning the first slice at the top of the circle for a cleaner visual layout. plt.axis("equal") ensures the pie renders as a true circle rather than an ellipse.

Data quality issue discovered and resolved: The initial chart rendered four slices instead of the expected two, because department values had been entered inconsistently through the CLI in Milestone 4 (e.g., "computer" versus "Computer Science", "mathematics" versus "Mathematics"). This is a realistic illustration of how free-text data entry, without validation or a constrained set of allowed values, can silently fragment what should be a single category into several. The issue was resolved with a small one-time utility script:

import sqlite3

conn = sqlite3.connect('data/student_success.db')
cursor = conn.cursor()

cursor.execute("UPDATE students SET department = 'Computer Science' WHERE department = 'computer'")
cursor.execute("UPDATE students SET department = 'Mathematics' WHERE department = 'mathematics'")

conn.commit()
conn.close()

The fix was verified via a direct SQL query confirming exactly two department values with counts of 4 (Computer Science) and 3 (Mathematics), and the temporary script was deleted afterward, since it served only a one-time data correction purpose rather than being part of the permanent codebase.

Verified output (post-fix): A clean two-slice pie chart showing 57.1% Computer Science and 42.9% Mathematics, saved to screenshots/department_distribution_pie_chart.png.

Scatter Plot: Math vs. Science Correlation

Code:
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
plt.show()

Explanation: The same pivot() reshaping technique introduced in Milestone 6 was reused to align each student's Math and Science scores. plt.scatter() plotted one point per student, with the marker size increased via s=100 for visibility, and plt.grid(True) added a light background grid to aid reading values off the axes.

Verified output: A tight, clearly upward-sloping diagonal pattern of points, visually confirming the 0.98 correlation coefficient calculated numerically in Milestone 6 — students scoring low in Math also scored low in Science, and vice versa, with no notable outliers. Saved to screenshots/math_vs_science_scatter.png.

Histogram: Score Distribution

Code:
def plot_score_distribution():
df = load_marks_dataframe()

plt.figure(figsize=(10, 6))
plt.hist(df["score"], bins=8, color="mediumseagreen", edgecolor="black")

plt.title("Distribution of All Scores")
plt.xlabel("Score")
plt.ylabel("Frequency")

plt.savefig("screenshots/score_distribution_histogram.png")
plt.show()

Explanation: plt.hist() grouped all 21 individual scores into 8 equal-width bins, showing how many scores fell into each range. edgecolor="black" added a visible border around each bar, distinguishing adjacent bars from one another.

Verified output: A distribution showing two visible clusters — one around the 38-45 range and a larger one around 88-95 — reflecting the deliberately varied strong and weak performer profiles designed into the test dataset in Milestone 5, rather than a single smooth central peak. Saved to screenshots/score_distribution_histogram.png.

Line Chart: Individual Student Score Trend

Code:
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
plt.show()

Explanation: plt.plot() connected a single student's scores across their three subjects in sequence, with marker="o" placing a visible dot at each actual data point rather than showing only a smooth line.

Documented limitation: This chart currently connects subject scores in the order they appear in the dataset, not scores across genuine time periods or semesters. It is presented explicitly as a demonstration of line-chart technique rather than a claim of tracking a student's improvement over time; true longitudinal trend analysis will become meaningful once semester-based historical data is introduced in a future milestone.

Verified output: A clear line connecting Rushika's Math (85.5), Science (90), and English (78) scores, saved to screenshots/student_score_trend_line_chart.png.

Complete File: visualization/charts.py

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

if name == "main":
plot_student_rankings()
plot_department_distribution()
plot_math_vs_science()
plot_score_distribution()
plot_student_score_trend(1)

Version Control

git add .
git commit -m "Add Matplotlib visualizations: bar chart, pie chart, scatter plot, histogram, and line chart"
git push

git status confirmed visualization/ and screenshots/ as new directories, with .gitignore continuing to correctly exclude venv/, pycache/, and the live database file.

Outcomes
The platform gained a complete visualization layer, converting numerical analytics from Milestones 5 and 6 into five distinct chart types saved as reusable image assets. This milestone also produced a genuine, documented data-quality fix — discovering and correcting inconsistently entered department names — reinforcing that visualization work often surfaces underlying data problems that purely numerical analysis can obscure.

Status: Complete. All five chart types generated, saved, and verified visually, all changes committed and pushed to the public repository.

Next: Milestone 8 — Student Dashboard, assembling analytics and visualizations into a cohesive student-facing feature within the platform.