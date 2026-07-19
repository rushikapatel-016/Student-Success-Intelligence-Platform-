# Milestone 5: Data Analytics with Pandas

## Objective
Introduce Pandas to transform raw database records into meaningful academic insights — class averages, subject-wise performance, student rankings, and automated identification of students needing academic support.

## Concepts Covered
- Loading SQL query results directly into a Pandas DataFrame
- SQL `JOIN` for combining data across related tables
- DataFrame aggregate functions: `.mean()`, `.idxmax()`, `.idxmin()`
- `.groupby()` and the split-apply-combine pattern
- Multi-column grouping
- `.sort_values()` for ranking
- Boolean filtering for conditional data selection

## File: `analytics/student_analytics.py`

### Data Loading

```python
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
```

**Key concepts**: A `JOIN` combines rows from `students` and `marks` based on matching `student_id` values — the same foreign key relationship established in Milestone 3. `pd.read_sql_query()` runs the SQL directly and loads results into a DataFrame, Pandas' core table-like data structure.

### Class-Wide Statistics

```python
def class_average(df):
    return df["score"].mean()

def highest_scoring_record(df):
    return df.loc[df["score"].idxmax()]

def lowest_scoring_record(df):
    return df.loc[df["score"].idxmin()]
```

**Key concepts**: `idxmax()`/`idxmin()` return the *index* of the extreme value, not the value itself; `.loc[]` retrieves the full row at that index — providing complete context (student, subject, score) rather than an isolated number.

### Subject-Wise Analysis

```python
def average_score_per_subject(df):
    return df.groupby("subject_name")["score"].mean()
```

**Key concepts**: `groupby()` splits the DataFrame into separate groups by unique column values, applies `.mean()` independently to each group, then combines the results — the split-apply-combine pattern central to Pandas-based analysis.

### Student Ranking

```python
def student_rankings(df):
    averages = df.groupby(["student_id", "name"])["score"].mean()
    ranked = averages.sort_values(ascending=False)
    return ranked
```

**Key concepts**: Grouping by two columns simultaneously creates one group per unique student. `sort_values(ascending=False)` orders results from highest to lowest.

### Weak Performer Detection

```python
def identify_weak_performers(df, threshold=60):
    averages = df.groupby(["student_id", "name"])["score"].mean()
    weak_students = averages[averages < threshold]
    return weak_students
```

**Key concepts**: Boolean filtering (`series[condition]`) selects only rows meeting a condition. A default parameter (`threshold=60`) makes the function reusable with different sensitivity levels without requiring the caller to always specify one.

## Test Data

Populated the database with 7 students across two departments and 21 mark records (3 subjects each), intentionally varied to include strong, average, and weak performers — enabling meaningful, non-trivial analytics results.

## Verified Results