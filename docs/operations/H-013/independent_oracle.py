"""Pre-implementation H-013 oracle: stdlib only; never imports product code.

Python relation arithmetic freezes expected values; independent temporary SQLite
queries cross-check every scope/group and actual M1 dependencies. --freeze is an
explicit CP-A operation, not a product test's update-on-failure escape hatch.
"""
import argparse
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sqlite3

HERE = Path(__file__).resolve().parent
E = [[1, 1, 9000], [2, 1, 6000], [3, 1, None], [1, 2, 10000],
     [1, 3, 7000], [2, 3, 8000], [4, 4, None], [2, 5, 10000]]
O = [[1, 1, 10, 'S1'], [2, 2, 11, 'S1'], [3, 1, 11, 'S2'],
     [4, 3, 10, 'S1'], [5, 1, 10, 'S1']]
KEYS = ['student_id', 'course_id', 'teacher_id', 'semester_id']
GROUPS = ['course_id', 'student_id', 'teacher_id', 'offering_id', 'semester_id']


def relation(enrollments):
    offerings = {r[0]: r for r in O}
    return [dict(student_id=s, offering_id=o, grade_units=g,
                 course_id=offerings[o][1], teacher_id=offerings[o][2],
                 semester_id=offerings[o][3]) for s, o, g in enrollments]


def average(raw):
    return (str((Decimal(raw[0]) / Decimal(raw[1]) / 100).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP)) if raw[1] else None)


def summary(rows):
    grades = [r['grade_units'] for r in rows if r['grade_units'] is not None]
    raw = [sum(grades), len(grades), len(rows)]
    return {'raw': raw, 'mean': average(raw),
            'distinct_students': len({r['student_id'] for r in rows}),
            'reason': 'no_rows' if not rows else 'no_grades' if not grades else None}


def grouped(rows, key):
    return [{'key': value, **summary([r for r in rows if r[key] == value])}
            for value in sorted({r[key] for r in rows})]


def top(rows):
    groups = [g for g in grouped(rows, 'course_id') if g['raw'][1]]
    if not groups:
        return []
    maximum = max(Fraction(g['raw'][0], g['raw'][1]) for g in groups)
    return [g['key'] for g in groups if Fraction(*g['raw'][:2]) == maximum]


def m1(enrollments):
    rows = [r for r in relation(enrollments) if r['semester_id'] == 'S1']
    courses = top(rows)
    cohort = sorted({r['student_id'] for r in rows if r['course_id'] in courses})
    return {'top_course_ids': courses, 'cohort_student_ids': cohort,
            'final': grouped([r for r in rows if r['student_id'] in cohort], 'student_id')}


def build():
    rows = relation(E)
    fixed = dict(student_id=2, course_id=1, teacher_id=10, semester_id='S1')
    scopes = []
    for n in range(5):
        for keys in combinations(KEYS, n):
            scope = {k: fixed[k] for k in keys}
            selected = [r for r in rows if all(r[k] == v for k, v in scope.items())]
            scopes.append({'scope': scope, **summary(selected),
                           'groups': {k: grouped(selected, k) for k in GROUPS},
                           'listing': [[r['student_id'], r['offering_id'], r['grade_units']]
                                       for r in selected], 'top_course_ids': top(selected)})
    tie = [[s, o, 8000 if (s, o) == (2, 1) else
            9000 if (s, o) == (1, 2) else g] for s, o, g in E]
    changed = [[s, o, 1000 if (s, o) == (2, 1) else g] for s, o, g in E]
    mutation_rows = relation(changed)
    return {'authority': 'H-013 CP-A; independently computed before dependent product tests',
            'fixtures': {'enrollments': E, 'offerings': O,
                         'students': [[1, 'Alex'], [2, 'Bea'], [3, 'Alex'], [4, 'Dana']]},
            'scopes': scopes,
            'mutations': {'grade_2_1_to_1000': {
                'enrollments': changed,
                'groups': {k: grouped(mutation_rows, k) for k in GROUPS},
                'filter_effects': {k: summary([r for r in mutation_rows if r[k] == fixed[k]])
                                   for k in KEYS}}},
            'm1': {'F1': {'enrollments': E, **m1(E)},
                   'F2': {'enrollments': E + [[3, 2, 5000]], **m1(E + [[3, 2, 5000]])},
                   'tie': {'enrollments': tie, **m1(tie)},
                   'empty': {'enrollments': [], **m1([])},
                   'no_grades': {'enrollments': [[s, o, None] for s, o, _ in E],
                                 **m1([[s, o, None] for s, o, _ in E])}},
            'zero': {'raw': [0, 1, 1], 'mean': '0.00'},
            'library': {'readers': [[1, 'Ada'], [2, 'Bob']],
                        'books': [[10, 'X'], [11, 'Y']],
                        'loans': [[1, 1, 10, 0], [2, 1, 11, 1], [3, 2, 10, 0]],
                        'expected': [[1, 'Ada', 1], [2, 'Bob', 1]],
                        'reader_without_loans': [[1, 'Ada', 1], [2, 'Bob', 1], [3, 'Cy', 0]],
                        'returned_mutation': [[1, 'Ada', 0], [2, 'Bob', 1]],
                        'all_returned': [[1, 'Ada', 0], [2, 'Bob', 0]]}}


def database(enrollments):
    db = sqlite3.connect(':memory:')
    db.execute('CREATE TABLE e(student_id INTEGER, offering_id INTEGER, grade_units INTEGER)')
    db.execute('CREATE TABLE o(offering_id INTEGER, course_id INTEGER, teacher_id INTEGER, semester_id TEXT)')
    db.executemany('INSERT INTO e VALUES(?,?,?)', enrollments)
    db.executemany('INSERT INTO o VALUES(?,?,?,?)', O)
    return db


FROM = ' FROM e JOIN o USING(offering_id) '
AGG = 'COALESCE(SUM(grade_units),0),COUNT(grade_units),COUNT(*),COUNT(DISTINCT student_id)'


def check(data):
    checks = []
    def equal(name, actual, expected):
        assert actual == expected, (name, actual, expected)
        checks.append(name)
    equal('frozen_reproducible', data, build())
    equal('anchor_global', data['scopes'][0]['raw'], [50000, 6, 8])
    equal('anchor_global_mean', data['scopes'][0]['mean'], '83.33')
    equal('anchor_F2_top', data['m1']['F2']['top_course_ids'], [1])
    equal('anchor_F2_cohort', data['m1']['F2']['cohort_student_ids'], [1, 2, 3])
    equal('anchor_F2_means', [g['mean'] for g in data['m1']['F2']['final']], ['95.00', '80.00', '50.00'])
    equal('anchor_F1_mean', [g['mean'] for g in data['m1']['F1']['final']], ['95.00'])
    equal('anchor_tie_means', [g['mean'] for g in data['m1']['tie']['final']], ['90.00', '90.00', None])
    db = database(E)
    for i, case in enumerate(data['scopes']):
        where = ' WHERE ' + ' AND '.join(k + '=:' + k for k in case['scope']) if case['scope'] else ''
        actual = list(db.execute('SELECT ' + AGG + FROM + where, case['scope']).fetchone())
        equal(f'scope_{i}_components', actual, case['raw'] + [case['distinct_students']])
        for key in GROUPS:
            actual = [list(r) for r in db.execute('SELECT ' + key + ',' + AGG + FROM + where + ' GROUP BY ' + key + ' ORDER BY ' + key, case['scope'])]
            expected = [[g['key']] + g['raw'] + [g['distinct_students']] for g in case['groups'][key]]
            equal(f'scope_{i}_group_{key}', actual, expected)
        actual = [list(r) for r in db.execute('SELECT student_id,offering_id,grade_units' + FROM + where, case['scope'])]
        equal(f'scope_{i}_listing', actual, case['listing'])
    db.close()
    mut = data['mutations']['grade_2_1_to_1000']
    db = database(mut['enrollments'])
    for key in GROUPS:
        actual = [list(r) for r in db.execute('SELECT ' + key + ',' + AGG + FROM + ' GROUP BY ' + key + ' ORDER BY ' + key)]
        expected = [[g['key']] + g['raw'] + [g['distinct_students']] for g in mut['groups'][key]]
        equal('mutation_group_' + key, actual, expected)
        equal('mutation_discriminates_' + key, mut['groups'][key] != data['scopes'][0]['groups'][key], True)
    for key, expected in mut['filter_effects'].items():
        value = dict(student_id=2, course_id=1, teacher_id=10, semester_id='S1')[key]
        actual = list(db.execute('SELECT ' + AGG + FROM + ' WHERE ' + key + '=?', [value]).fetchone())
        equal('mutation_filter_' + key, actual, expected['raw'] + [expected['distinct_students']])
        original = next(c for c in data['scopes'] if c['scope'] == {key: value})
        equal('mutation_filter_discriminates_' + key, expected['raw'] != original['raw'], True)
    db.close()
    for name, fixture in data['m1'].items():
        db = database(fixture['enrollments'])
        raw = list(db.execute('SELECT course_id,SUM(grade_units),COUNT(grade_units)' + FROM + "WHERE semester_id='S1' GROUP BY course_id HAVING COUNT(grade_units)>0"))
        max_fraction = max((Fraction(r[1], r[2]) for r in raw), default=None)
        ids = sorted(r[0] for r in raw if Fraction(r[1], r[2]) == max_fraction)
        equal(name + '_sql_top', ids, fixture['top_course_ids'])
        # Actual SQL dependency values become the next query's bound parameters.
        cohort = sorted({r[0] for r in db.execute('SELECT DISTINCT student_id' + FROM + "WHERE semester_id='S1' AND course_id IN (" + ','.join('?' for _ in ids) + ')', ids)}) if ids else []
        equal(name + '_sql_cohort', cohort, fixture['cohort_student_ids'])
        final = [list(r) for r in db.execute('SELECT student_id,' + AGG + FROM + "WHERE semester_id='S1' AND student_id IN (" + ','.join('?' for _ in cohort) + ') GROUP BY student_id ORDER BY student_id', cohort)] if cohort else []
        equal(name + '_sql_final', final, [[g['key']] + g['raw'] + [g['distinct_students']] for g in fixture['final']])
        db.close()
    lib = data['library']
    db = sqlite3.connect(':memory:')
    db.executescript('CREATE TABLE readers(id INTEGER,name TEXT);CREATE TABLE loans(id INTEGER,reader_id INTEGER,book_id INTEGER,returned INTEGER);')
    db.executemany('INSERT INTO readers VALUES(?,?)', lib['readers'])
    db.executemany('INSERT INTO loans VALUES(?,?,?,?)', lib['loans'])
    sql = 'SELECT r.id,r.name,COUNT(l.id) FROM readers r LEFT JOIN loans l ON r.id=l.reader_id AND l.returned=0 GROUP BY r.id,r.name ORDER BY r.id'
    equal('library_baseline', [list(r) for r in db.execute(sql)], lib['expected'])
    db.execute("INSERT INTO readers VALUES(3,'Cy')")
    equal('library_reader_zero', [list(r) for r in db.execute(sql)], lib['reader_without_loans'])
    db.execute('DELETE FROM readers WHERE id=3')
    db.execute('UPDATE loans SET returned=1 WHERE id=1')
    equal('library_returned_mutation', [list(r) for r in db.execute(sql)], lib['returned_mutation'])
    db.execute('UPDATE loans SET returned=1')
    equal('library_all_returned', [list(r) for r in db.execute(sql)], lib['all_returned'])
    db.close()
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze', action='store_true')
    args = parser.parse_args()
    frozen = HERE / 'frozen-oracle.json'
    if args.freeze:
        if frozen.exists():
            raise SystemExit('Refusing to overwrite frozen oracle; inspect/version explicitly')
        frozen.write_text(json.dumps(build(), indent=2) + '\n')
    data = json.loads(frozen.read_text())
    checks = check(data)
    receipt = {'status': 'passed', 'checks': len(checks), 'check_names': checks,
               'oracle_sha256': hashlib.sha256(frozen.read_bytes()).hexdigest(),
               'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'sqlite_version': sqlite3.sqlite_version, 'product_imports': False,
               'database': 'temporary in-memory only', 'live_calls': 0,
               'claim': 'independent oracle cross-check, not product acceptance or NL accuracy'}
    (HERE / 'oracle-validation.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: receipt[k] for k in ['status', 'checks', 'oracle_sha256']}))


if __name__ == '__main__':
    main()
