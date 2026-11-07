from pathlib import Path

import pytest

from universitydb.db import initialize
from universitydb.domain import SPEC

ROOT = Path(__file__).resolve().parents[1]
QUESTION = (
    "Какова средняя оценка Bea (student_id=2) по DB (course_id=1) "
    "у Kim (teacher_id=10) в семестре S1?"
)
SCOPE = {"student_id": 2, "course_id": 1, "teacher_id": 10, "semester_id": "S1"}
SQL = """SELECT COALESCE(SUM(e.grade_units),0) AS sum_units,
COUNT(e.grade_units) AS graded_count, COUNT(*) AS enrollment_count
FROM Enrollments e JOIN Offerings o ON e.offering_id = o.offering_id
WHERE e.student_id = :student_id AND o.course_id = :course_id
AND o.teacher_id = :teacher_id AND o.semester_id = :semester_id"""


def outputs(scope=None, sql=SQL):
    scope = scope or SCOPE
    spec = SPEC.model_dump()
    plan = {
        "version": "1",
        "steps": [
            {
                "step_id": "s6",
                "depends_on": [],
                "purpose": "Mean",
                "result_refs": [],
                "result_spec": spec,
            }
        ],
        "needs_clarification": False,
        "clarification_field": None,
    }
    proposal = {
        "version": "1",
        "step_id": "s6",
        "result_spec": spec,
        "sql": sql,
        "parameters": [
            {
                "name": k,
                "type": "text" if isinstance(v, str) else "integer",
                "integer_value": None if isinstance(v, str) else v,
                "text_value": v if isinstance(v, str) else None,
            }
            for k, v in scope.items()
        ],
        "expected_columns": ["sum_units", "graded_count", "enrollment_count"],
        "result_kind": "aggregate",
        "explanation": "Scoped mean",
    }
    return [plan, proposal]


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "fixture.db"
    initialize(path, ROOT / "resources")
    return path
