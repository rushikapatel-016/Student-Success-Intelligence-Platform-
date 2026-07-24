# Student Success Intelligence Platform — Project Overview

## Summary

The Student Success Intelligence Platform is a Python-based academic management and analytics system built to help students track their own performance and help faculty identify students who need academic support. Built incrementally across 11 structured milestones, the project demonstrates database design, object-oriented programming, data analysis, statistical computation, data visualization, full-stack CLI application development, and automated testing.

## Problem Statement

Colleges collect large amounts of student data — attendance, marks, assignments, quiz scores — but this data often goes unanalyzed until after examinations, when it's too late for students to improve. This platform surfaces performance trends and at-risk students proactively, using real data analysis rather than manual review.

## Technology Stack

- **Language**: Python 3
- **Database**: SQLite
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Matplotlib
- **Testing**: Python's built-in `unittest`
- **Version Control**: Git & GitHub

## Architecture

The project follows a layered architecture (Data → Domain → Analysis → Presentation), detailed fully in [ARCHITECTURE.md](ARCHITECTURE.md). This design enabled significant code reuse — the same `Student` and `Marks` classes, and the same analytics functions, power the general CLI, both role-specific dashboards, and the automated test suite, without duplication.

## Database Design

Three tables (`students`, `subjects`, `marks`) with a foreign key relationship connecting students to their marks records, detailed fully in [ER_DIAGRAM.md](ER_DIAGRAM.md).

## Milestone Summary

| # | Milestone | Key Deliverable |
|---|---|---|
| 1 | Project Setup | Environment, Git/GitHub, professional folder structure |
| 2 | Database & OOP | SQLite schema, `Student` class with save functionality |
| 3 | Relationships | `subjects`/`marks` tables, foreign keys, `Marks` class |
| 4 | CRUD + CLI | Full CRUD operations, input validation, working CLI |
| 5 | Pandas Analytics | Class averages, rankings, weak-performer detection |
| 6 | NumPy Statistics | Standard deviation, correlation, GPA, Performance Index |
| 7 | Visualizations | Bar, pie, scatter, histogram, and line charts |
| 8 | Student Dashboard | Login, profile, marks/GPA, chart, progress report |
| 9 | Faculty Dashboard | Student/marks management, class analytics, weak-performer alerts |
| 10 | Testing & Validation | 7 automated unit tests, manual testing checklist |
| 11 | Polish & Documentation | Architecture docs, ER diagram, updated README, final showcase |

Full, detailed documentation for each milestone — including debugging notes and design rationale — is available in this `docs/` folder as `milestone-1.md` through `milestone-10.md`.

## Notable Bugs Found and Fixed

This project's development process deliberately preserved and documented real debugging experiences, rather than only showing polished final code:

1. **False success on invalid updates/deletes** (Milestone 4): SQL `UPDATE`/`DELETE` statements silently succeed even when zero rows match. Fixed using `cursor.rowcount` to verify an actual change occurred before reporting success.
2. **Disabled foreign key enforcement** (Milestone 9): SQLite disables foreign key constraints by default; despite declaring the relationship in Milestone 3, it was never actually enforced until `PRAGMA foreign_keys = ON` was added.
3. **Data fragmentation from free-text entry** (Milestones 7 and 9): Inconsistent capitalization ("computer" vs. "Computer Science", "Math" vs. "mathematics") silently created duplicate categories in both department and subject fields — resolved with data cleanup and added validation.
4. **Incorrectly scoped test mocking** (Milestone 10): An initial attempt to redirect database connections during testing patched the wrong module reference, causing tests to run against the real production database rather than an isolated test database.

## Known Limitations & Future Work

- No password-based authentication; dashboard "login" is currently identity lookup by roll number only
- `marks.subject_name` is free text rather than a formal foreign key to the `subjects` table
- Machine learning-based grade/risk prediction not yet implemented
- No web-based interface (CLI only)

## Skills Demonstrated

Python fundamentals, object-oriented programming, SQL and relational database design, Pandas and NumPy for data analysis, Matplotlib for visualization, Git/GitHub version control, automated testing with `unittest`, debugging and root-cause analysis, and technical documentation.

## Author

Rushika Patel
GitHub: [rushikapatel-016](https://github.com/rushikapatel-016)
Repository: [Student-Success-Intelligence-Platform](https://github.com/rushikapatel-016/Student-Success-Intelligence-Platform-)