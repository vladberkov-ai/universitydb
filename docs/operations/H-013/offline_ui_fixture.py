"""Build explicit scripted SQL proposals for isolated offline UI evidence.

No provider generation, result fabrication, credential loading or persistent DB
changes. Real SQLite+graph compute every rendered result. Frozen independent
expected values remain the authority, never these proposal-building helpers.
"""

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests"))
from ui_fixtures import plan, proposal, step

from universitydb.domain import University, make_spec
from universitydb.library import SPEC as LIBRARY_SPEC
from universitydb.library import Library

S6 = {"student_id": 2, "course_id": 1, "teacher_id": 10, "semester_id": "S1"}


def m1_outputs():
    domain = University()
    top = make_spec("top_course", "course_id")
    cohort = make_spec("student_ids")
    means = make_spec("grade_mean", "student_id")
    scope = {"semester_id": "S1"}
    return [
        plan(
            step(top, "top"),
            step(
                cohort,
                "cohort",
                [
                    {
                        "from_step": "top",
                        "column": "course_id",
                        "type": "integer",
                        "bind_as": "course_ids",
                    }
                ],
            ),
            step(
                means,
                "means",
                [
                    {
                        "from_step": "cohort",
                        "column": "student_id",
                        "type": "integer",
                        "bind_as": "student_ids",
                    }
                ],
            ),
        ),
        proposal(domain, top, scope, "top"),
        proposal(domain, cohort, scope, "cohort", {"course_ids": [2]}),
        proposal(domain, means, scope, "means", {"student_ids": [1]}),
    ]


def fixture(full=False):
    domain = University()
    mean = make_spec("grade_mean")
    s6 = [plan(step(mean)), proposal(domain, mean, S6)]
    clarification = [plan(step(mean)), proposal(domain, mean, {"student_id": 1})]
    invalid = deepcopy(s6[1])
    invalid["sql"] = invalid["sql"].replace("e.grade_units", "e.unknown_grade_units")
    repair = [s6[0], invalid, s6[1]]
    refusal = [
        {
            "injected_error": {
                "code": "PROVIDER_REFUSAL",
                "message": "Explicit offline injected refusal.",
            }
        }
    ]
    return {
        "university-v1": s6 + clarification + (m1_outputs() if full else []) + repair + refusal,
        "library-v1": [plan(step(LIBRARY_SPEC)), proposal(Library(), LIBRARY_SPEC, {})],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()
    args.output.write_text(json.dumps(fixture(args.full), indent=2) + "\n")
    print("Saved offline/injected SQL proposals; real_provider_called=false")
