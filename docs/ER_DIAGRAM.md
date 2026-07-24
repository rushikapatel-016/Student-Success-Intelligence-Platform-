# Entity-Relationship Diagram (Text Format)

## Entities and Attributes

### students
- student_id (PRIMARY KEY, INTEGER, AUTOINCREMENT)
- name (TEXT, NOT NULL)
- roll_number (TEXT, NOT NULL, UNIQUE)
- email (TEXT)
- department (TEXT)

### subjects
- subject_id (PRIMARY KEY, INTEGER, AUTOINCREMENT)
- subject_name (TEXT, NOT NULL, UNIQUE)

### marks
- mark_id (PRIMARY KEY, INTEGER, AUTOINCREMENT)
- student_id (INTEGER, NOT NULL, FOREIGN KEY -> students.student_id)
- subject_name (TEXT, NOT NULL)
- score (REAL, NOT NULL)

## Relationships

students (1) ────────< marks (many)
    student_id              student_id (FK)

    One student can have many mark records.
    Each mark record belongs to exactly one student.
    Enforced via: FOREIGN KEY (student_id) REFERENCES students (student_id)
    with PRAGMA foreign_keys = ON (see Milestone 9 for the enforcement fix).

## Visual Representation

┌─────────────────────┐
│      students         │
├─────────────────────┤
│ PK  student_id        │
│     name              │
│     roll_number (UQ)  │
│     email             │
│     department        │
└──────────┬──────────┘
           │
           │ 1
           │
           │ has many
           │
           │ many
┌──────────▼──────────┐
│        marks          │
├─────────────────────┤
│ PK  mark_id            │
│ FK  student_id         │
│     subject_name       │
│     score              │
└─────────────────────┘

┌─────────────────────┐
│      subjects         │
├─────────────────────┤
│ PK  subject_id         │
│     subject_name (UQ)  │
└─────────────────────┘

Note: The subjects table currently exists as an independent
reference table and is not yet formally linked via foreign key
to marks.subject_name, which is stored as free text. This is
a documented area for future refinement - validated at the
application layer (see dashboards/faculty_dashboard.py,
VALID_SUBJECTS list) rather than enforced at the database level.

## Design Notes

- One-to-Many Relationship: The only formal foreign key relationship in the schema is students to marks, a classic one-to-many pattern, where one student record relates to zero or more mark records.

- subjects Table Limitation: The subjects table was created in Milestone 3 as a reference table, but marks.subject_name stores subject names as plain text rather than a foreign key reference to subjects.subject_id. This design decision was made for simplicity at the time, and was later compensated for at the application layer with a hardcoded VALID_SUBJECTS list (Milestone 9) after a real data-fragmentation bug ("Math" vs "mathematics") was discovered. A more complete schema would formally link marks to subjects via foreign key, eliminating the need for application-layer validation, a natural improvement for a future milestone.