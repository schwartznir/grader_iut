"""The goal of the module is to grade the python submissions downloaded from e-campus Paris Saclay"""

import os
import signal
import pandas as pd
import shutil
import numpy as np
import csv
import zipfile
import sys
from pylint.lint import Run

from tests import TESTS_INV as TESTS

csv_name = 'grades_names.csv'
TP_NAME = 'TP22'
curr_zip = TP_NAME+'.zip'
functionname = 'invmat'
IS_EXACT = 1  # 1 is the students' result should be exactly like the test code. 0 otherwise.
PROXIMITY = 0.01  # If not exact, demand proximity of PROXIMITY between student's solution and the test solution


def parse_contents(currzip=curr_zip):
    """A function which extracts a zip file containing students' assignments
    in a format «lastname firstname_sn_submission to a temporary created folder
    temp_assignments. It then produces a new zip file new_zip.zip which can be
    manipulated by py-garder as well as a list of names in format csv"""
    os.makedirs('temp_assignments', exist_ok=True)
    names = []

    # Extract the contents of the old file
    with zipfile.ZipFile(currzip, "r") as oldzip:
        oldzip.extractall(os.getcwd() + '/temp_assignments')

    assignments_path = os.getcwd() + '/temp_assignments/'
    submissions = os.listdir(assignments_path)

    with open(csv_name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['first and last name', 'PEP grade (out of 5)', 'Tests grade'])

    # Append students names to the csv and rename their submission uniformly
        for submission in submissions:
            split_submission = submission.split('_')
            first_and_last_name = split_submission[0]
            names.append(first_and_last_name)

            curr_submission = assignments_path + '/' + submission
            files = os.listdir(curr_submission)

            if len(files) == 1:
                os.rename(curr_submission + '/' + files[0], curr_submission + '/submission.py')
            else:
                pass

    return [assignments_path + submission + '/submission.py' for submission in submissions], names


def grader(submissions, names):
    """A function which goes over each submission and grades it. The grading is out of 20 pts
    15 pts are given for passing numerical tests and 5 for following PEP 8"""
    grades = pd.DataFrame(columns=['name', 'pep grade/5', 'practical tests grade/15', 'final grade'])

    for name in names:
        curr_line = pd.Series({'name': name, 'pep grade/5': 0,
                               'practical tests grade/15': 0,
                               'final grade': 0})

        grades = grades.append(curr_line, ignore_index=True)

    grades_w_pep = pylint_eval(submissions, grades)
    grades_w_practical = num_eval(submissions, grades_w_pep)

    return grades_w_practical


def num_eval(submissions, grades):
    # Evaluate each of the submissions in terms of desired outputs specified in tests.py
    pts_per_test = 15 / len(TESTS)
    updated_grades = grades.copy()
    idx = 0

    for sub in submissions:
        curr_dir = sub.replace('submission.py', '')
        sys.path.insert(1, curr_dir)
        grade = 0

        for params in TESTS:
            try:
                if test(params[0], params[1]) == 1:
                    grade += pts_per_test
            except:
                continue

        updated_grades.at[idx, 'practical tests grade/15'] = grade
        updated_grades.at[idx, 'final grade'] = updated_grades.at[idx, 'practical tests grade/15'] + \
                                                updated_grades.at[idx, 'pep grade/5']
        sys.path.remove(curr_dir)
        idx += 1

    return updated_grades


def handler(signum, frame):
    print("It takes too much time to execute the code. Quitting")
    raise TimeoutError


class TimeOutError(RuntimeError):
    pass


def test(inp, right_output):
    # Test if a student's function gives a correct output
    try:
        try:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(25)
            import submission
            student_func = getattr(submission, functionname)
            stud_output = student_func(inp)
        except:
            return 0
        if IS_EXACT:
            np.testing.assert_equal(stud_output, right_output)
            return 1
        else:
            return int(np.abs(stud_output - right_output) < PROXIMITY)
    except:
        return 0


def pylint_eval(submissions, grades):
    """Run pylint on a given python file and store the score in a dedicated csv"""

    grades_pep = []

    for submission in submissions:
        pep_run = Run(submission, do_exit=False)
        grade = pep_run.linter.stats['global_note']

        if grade >= 0:
            grades_pep.append(grade/2)
        else:
            grades_pep.append(0.0)

    # grades_with_shift = [np.floor(5.0, float(grade + np.abs(stats.mean(grades_wo_shift))))
    # for grade in grades_wo_shift]
    grades['pep grade/5'] = grades_pep
    return grades


def main():
    """Main caller - converts a given zip from the platform e-campus of Université Paris Saclay
    to a formatted zip. On that zip one runs pygrader and evaluates the performance of each code
    under several tests specified in «tests» folder"""
    # parse the zip downloaded from e-ecampus
    submissions, names = parse_contents()
    grades = grader(submissions, names)
    grades.to_csv('grades for '+functionname+'.csv', index=True)
    shutil.rmtree(os.getcwd()+'/temp_assignments')

main()
