# Database schema and seed

Sources: [schema](../resources/schema.sql), [seed](../resources/seed.sql).
SQLite STRICT tables, foreign keys; grade_units is nullable integer hundredths in0..10000.
Students and Teachers require nonblank names. Offerings links course/teacher/semester
and section; Enrollments links a student to an offering and optional grade.

Seed:4students,2teachers,3courses,2semesters,5offerings,8enrollments, all synthetic.
Two Alex records intentionally have distinct IDs. Bea/student2 has two S1 DB/Kim
enrollments with60.00 and100.00; expected mean80.00. Alex/student1 matches one90.00.
NULL is not zero. Primary/foreign keys, grade range and offering uniqueness are enforced.

The UI initializes runtime/university-v1.db (or runtime/library-v1.db for Library) on first dataset use if absent. To create a
separate inspection database explicitly, from the installed checkout:
```bash
uv run --locked python -c 'from pathlib import Path; from universitydb.db import initialize; initialize(Path("runtime/inspection.db"), Path("resources"))'
```
The initializer refuses to overwrite an existing file. Choose a new filename if needed;
do not remove the live DB or spending ledger as part of verification.
Generated SQL uses a separate read-only worker; provisioning is a trusted startup step.
An SQLite binary is not shipped: SQL schema and seed are the reproducible deliverables.

## Library

[Schema](../resources/library/schema.sql) and [seed](../resources/library/seed.sql)
define Readers, Books and Loans. The synthetic seed has two readers (Ada/Bob), two
books and three loans; each reader has one unreturned loan. Returned loans do not
count; readers with no open loans retain a zero row. [Library adapter](../src/universitydb/library.py)
owns these rules; the core graph, DB safety, provider, trace and UI remain common.

```bash
uv run --locked python -c 'from pathlib import Path; from universitydb.db import initialize; initialize(Path("runtime/library-inspection.db"), Path("resources/library"))'
```

University means equally weight graded enrollments across all selected offerings,
including retakes. NULL is excluded, zero is included. Omitted filters include all
semesters with explicit scope. Top results retain all exact ties before display
rounding. Both datasets require the supported DELETE journal mode.
