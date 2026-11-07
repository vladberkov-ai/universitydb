"""Independent frozen relation oracle checks product adaptation, never derives expectations."""

import sqlite3

from test_i2_domains import ORACLE, execute_spec

from universitydb.domain import GROUPS, make_spec


def test_every_group_and_filter_mutation_discriminates(database):
    mutant = ORACLE["mutations"]["grade_2_1_to_1000"]
    with sqlite3.connect(database) as conn:
        conn.execute("UPDATE Enrollments SET grade_units=1000 WHERE student_id=2 AND offering_id=1")
    for group in GROUPS:
        raw, adapted = execute_spec(database, make_spec("grade_mean", group), {})
        expected = mutant["groups"][group]
        assert raw == [[g["key"], *g["raw"]] for g in expected]
        assert adapted["answer"]["rows"] == [[g["key"], g["mean"], *g["raw"][1:]] for g in expected]
        assert expected != ORACLE["scopes"][0]["groups"][group]
    fixed = {"student_id": 2, "course_id": 1, "teacher_id": 10, "semester_id": "S1"}
    for key, expected in mutant["filter_effects"].items():
        raw, adapted = execute_spec(database, make_spec("grade_mean"), {key: fixed[key]})
        assert raw == [expected["raw"]]
        assert adapted["answer"]["rows"][0][0] == expected["mean"]
        baseline = next(c for c in ORACLE["scopes"] if c["scope"] == {key: fixed[key]})
        assert expected["raw"] != baseline["raw"]


def test_independent_oracle_detects_plausible_safe_wrong_join_and_average_of_means(database):
    # This deliberately bypasses product SQL validation to prove the independent
    # semantic oracle catches safe-but-wrong SQL, rather than blessing SELECT safety.
    with sqlite3.connect(database) as conn:
        wrong_join = conn.execute(
            "SELECT COALESCE(SUM(e.grade_units),0),COUNT(e.grade_units),COUNT(*) FROM Enrollments e JOIN Offerings o ON e.student_id=o.offering_id WHERE o.semester_id='S1'"
        ).fetchone()
        assert (
            list(wrong_join)
            != next(c for c in ORACLE["scopes"] if c["scope"] == {"semester_id": "S1"})["raw"]
        )
        wrong_mean = conn.execute(
            "SELECT AVG(m) FROM (SELECT AVG(e.grade_units)/100.0 AS m FROM Enrollments e JOIN Offerings o USING(offering_id) WHERE o.semester_id='S1' GROUP BY o.course_id)"
        ).fetchone()[0]
        expected = next(c for c in ORACLE["scopes"] if c["scope"] == {"semester_id": "S1"})
        assert f"{wrong_mean:.2f}" != expected["mean"]
