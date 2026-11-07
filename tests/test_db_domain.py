import sqlite3
import time
from copy import deepcopy

import pytest
from conftest import QUESTION, SCOPE, SQL, outputs

from universitydb import db
from universitydb.contracts import Failure, SQLProposal
from universitydb.domain import University


def test_fixture_constraints(database):
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA foreign_keys=ON")
        assert [
            connection.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            for t in ("Students", "Teachers", "Courses", "Offerings", "Enrollments")
        ] == [4, 2, 3, 5, 8]
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
        assert connection.execute(
            "SELECT COUNT(*) FROM Enrollments WHERE grade_units IS NULL"
        ).fetchone() == (2,)
        for statement in (
            "INSERT INTO Students VALUES(5,' ')",
            "INSERT INTO Enrollments VALUES(99,1,5000)",
            "INSERT INTO Enrollments VALUES(4,1,10001)",
            "INSERT INTO Enrollments VALUES(1,1,9000)",
        ):
            with pytest.raises(sqlite3.IntegrityError):
                connection.execute(statement)
    assert db.inspect(database, University.tables)["db_sha256"] == db.file_hash(database)


def test_raw_s6_and_formatter(database):
    domain = University()
    assert domain.resolve(QUESTION) == SCOPE
    domain.validate_sql(SQLProposal.model_validate(outputs()[1]), SCOPE)
    raw = db.execute(database, SQL, SCOPE, domain.tables, domain.functions)
    assert raw["columns"] == [
        {"name": n, "type": "integer"} for n in ["sum_units", "graded_count", "enrollment_count"]
    ]
    assert raw["rows"] == [[16000, 2, 2]]
    assert all(type(v) is int for v in raw["rows"][0])
    assert domain.answer(raw["rows"], SCOPE)["rows"] == [["80.00", 2, 2]]


@pytest.mark.parametrize(
    "removed,values,expected",
    [
        ("student_id", None, [25000, 3, 4]),
        ("course_id", (6, 2, 10, "S1", "X", 2000), [18000, 3, 3]),
        ("teacher_id", (6, 1, 11, "S1", "X", 3000), [19000, 3, 3]),
        ("semester_id", (6, 1, 10, "S2", "X", 4000), [20000, 3, 3]),
    ],
)
def test_each_filter_has_independent_discriminating_oracle(database, removed, values, expected):
    # Each synthetic row differs from S6 in exactly one dimension. Expected sums are manual.
    with sqlite3.connect(database) as connection:
        if values:
            connection.execute("INSERT INTO Offerings VALUES(?,?,?,?,?)", values[:5])
            connection.execute("INSERT INTO Enrollments VALUES(2,6,?)", (values[5],))
        assert list(connection.execute(SQL, SCOPE).fetchone()) == [16000, 2, 2]
        predicate = {
            "student_id": "e.student_id",
            "course_id": "o.course_id",
            "teacher_id": "o.teacher_id",
            "semester_id": "o.semester_id",
        }[removed]
        mutant = SQL.replace(f"{predicate} = :{removed}", "1=1")
        assert list(connection.execute(mutant, SCOPE).fetchone()) == expected
        assert expected != [16000, 2, 2]
    proposal = outputs(sql=mutant)[1]
    with pytest.raises(Failure, match="four exact"):
        University().validate_sql(SQLProposal.model_validate(proposal), SCOPE)


@pytest.mark.parametrize(
    "rows,average,reason",
    [
        ([[0, 0, 0]], None, "no_rows"),
        ([[0, 0, 1]], None, "no_grades"),
        ([[0, 1, 1]], "0.00", None),
        ([[1, 1, 1]], "0.01", None),
    ],
)
def test_formatter_zero_cases(rows, average, reason):
    answer = University().answer(rows, SCOPE)
    assert answer["rows"][0][0] == average
    assert answer["empty_reason"] == reason


@pytest.mark.parametrize(
    "rows", [[[None, 0, 0]], [[1, 0, 1]], [[10001, 1, 1]], [[0, 2, 1]], [[True, 1, 1]]]
)
def test_bad_components_fail(rows):
    with pytest.raises(Failure):
        University().answer(rows, SCOPE)


@pytest.mark.parametrize(
    "sql",
    [
        "DELETE FROM Students",
        "DROP TABLE Students",
        "ATTACH DATABASE ':memory:' AS other",
        "PRAGMA user_version",
        "SELECT load_extension('x')",
        "SELECT name FROM sqlite_master",
        "SELECT * FROM Enrollments; DELETE FROM Students",
        "SELECT random()",
        "WITH x AS (SELECT * FROM sqlite_master) SELECT * FROM x",
    ],
)
def test_sqlite_authorizer_real_denials_and_db_unchanged(database, sql):
    before = db.file_hash(database)
    with pytest.raises(Failure):
        db.execute(database, sql, {}, University.tables, University.functions)
    assert db.file_hash(database) == before


@pytest.mark.parametrize(
    "mutation",
    [
        lambda s: s + "; SELECT 1",
        lambda s: s + " UNION SELECT 1,2,3",
        lambda s: s.replace("o.semester_id = :semester_id", "o.semester_id = :semester_id OR 1=1"),
        lambda s: s.replace("e.offering_id = o.offering_id", "1=1"),
        lambda s: s.replace("SUM(e.grade_units)", "SUM(e.grade_units)*2"),
        lambda s: s + " LIMIT 1",
        lambda s: s.replace(" JOIN ", " LEFT JOIN "),
        lambda s: s.replace("Enrollments e", "main.Enrollments e"),
        lambda s: s.replace(":student_id", "2"),
    ],
)
def test_narrow_ast_rejects_subtle_changes(mutation):
    proposal = SQLProposal.model_validate(outputs(sql=mutation(SQL))[1])
    with pytest.raises(Failure):
        University().validate_sql(proposal, SCOPE)


def test_db_timeout_and_separate_watchdog(database):
    sql = "SELECT count(*) FROM Enrollments a, Enrollments b, Enrollments c, Enrollments d, Enrollments e, Enrollments f, Enrollments g, Enrollments h, Enrollments i, Enrollments j"
    started = time.monotonic()
    with pytest.raises(Failure) as error:
        db.execute(database, sql, {}, University.tables, University.functions, timeout=0.01)
    assert error.value.code == "SQL_TIMEOUT"
    assert time.monotonic() - started < 3
    started = time.monotonic()
    with pytest.raises(Failure, match="watchdog"):
        db.execute(
            database, sql, {}, University.tables, University.functions, timeout=20, watchdog=0.2
        )
    assert time.monotonic() - started < 1


def test_scope_bindings_fail_closed():
    value = deepcopy(outputs()[1])
    value["parameters"][0]["integer_value"] = 1
    with pytest.raises(Failure):
        University().validate_sql(SQLProposal.model_validate(value), SCOPE)
