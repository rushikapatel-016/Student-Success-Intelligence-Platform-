# Architecture Overview

## System Design Philosophy

This project follows a layered architecture, where each folder has a single, clear responsibility, and dependencies flow in one direction only — upward layers depend on lower layers, never the reverse. This separation was established from Milestone 1 and maintained consistently through all 11 milestones, enabling significant code reuse without duplication (for example, both dashboards and the class-wide analytics all share the same underlying Student, Marks, and analytics functions).

## Layers

### 1. Data Layer — database/
Responsible solely for establishing SQLite connections and defining table schemas. Exposes create_connection(), used by every other layer, and create_tables() / create_subjects_table() / create_marks_table(), run once to initialize the database structure. Enables foreign key constraint enforcement via PRAGMA foreign_keys = ON (added in Milestone 9, after discovering it was silently disabled by default).

### 2. Domain Layer — models/
Contains Student and Marks, the platform's core business entities, implemented as Python classes. Each class encapsulates its own validation logic, CRUD operations (Create, Read, Update, Delete), and error handling — depending only on the Data Layer beneath it.

### 3. Analysis Layer — analytics/ and visualization/
- analytics/student_analytics.py: Pandas-based calculations (class averages, subject breakdowns, rankings, weak-performer identification)
- analytics/statistics_analysis.py: NumPy-based statistical measures (standard deviation, variance, correlation, GPA, Performance Index)
- visualization/charts.py: Matplotlib-based chart generation, consuming the analytics layer's functions to produce bar charts, pie charts, scatter plots, histograms, and line charts

This layer depends on the Domain and Data layers but has no awareness of how its output will ultimately be presented to a user.

### 4. Presentation Layer — app.py and dashboards/
- app.py: A general-purpose CLI exposing full CRUD operations on students
- dashboards/student_dashboard.py: A role-specific interface for an individual student to view their own profile, marks, GPA, chart, and progress report
- dashboards/faculty_dashboard.py: A role-specific interface for faculty to manage students, record marks, and view class-wide analytics and weak-performer alerts

This layer is the only one that directly interacts with a human user, and contains no business logic itself — it composes and orchestrates calls into the layers beneath it.

### 5. Storage — data/student_success.db
The physical SQLite database file, excluded from version control via .gitignore, since it contains generated data rather than source code, and is fully reproducible by running database/db_connection.py.

## Testing — tests/
Automated unit tests (unittest) verify the Domain Layer's behavior in isolation, using a separate, temporary test database created and destroyed for each test run, ensuring the real database is never at risk during testing.

## Key Architectural Decisions

- Separation of concerns: Each folder has exactly one responsibility, making the codebase navigable and each piece independently testable.
- Reuse over duplication: Both dashboards, the CLI, and the test suite all call into the same underlying Student and Marks classes and the same analytics functions — no logic is ever copy-pasted between files.
- Fail loudly, but gracefully: Errors (invalid input, missing records, foreign key violations) are caught and reported clearly rather than causing silent incorrect behavior or unhandled crashes — a principle reinforced repeatedly after real bugs were found in Milestones 4 and 9.