PRAGMA foreign_keys = ON;
CREATE TABLE Students (student_id INTEGER PRIMARY KEY, name TEXT NOT NULL CHECK(length(trim(name))>0)) STRICT;
CREATE TABLE Teachers (teacher_id INTEGER PRIMARY KEY, name TEXT NOT NULL CHECK(length(trim(name))>0)) STRICT;
CREATE TABLE Courses (course_id INTEGER PRIMARY KEY, code TEXT NOT NULL UNIQUE, title TEXT NOT NULL CHECK(length(trim(title))>0)) STRICT;
CREATE TABLE Semesters (semester_id TEXT PRIMARY KEY, starts_on TEXT NOT NULL, ends_on TEXT NOT NULL, CHECK(starts_on<=ends_on)) STRICT;
CREATE TABLE Offerings (offering_id INTEGER PRIMARY KEY, course_id INTEGER NOT NULL REFERENCES Courses, teacher_id INTEGER NOT NULL REFERENCES Teachers, semester_id TEXT NOT NULL REFERENCES Semesters, section TEXT NOT NULL, UNIQUE(course_id,semester_id,section)) STRICT;
CREATE TABLE Enrollments (student_id INTEGER NOT NULL REFERENCES Students, offering_id INTEGER NOT NULL REFERENCES Offerings, grade_units INTEGER CHECK(grade_units BETWEEN 0 AND 10000), PRIMARY KEY(student_id,offering_id)) STRICT;
