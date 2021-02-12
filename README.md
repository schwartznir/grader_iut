# grader_iut

A simple code extracting and grading students' code submissions in the course M398 given at Institut universitaire technologique d'Orsay in 2020-2021. The code requires one to download students' submissions zip manually from the moodle platform of the university, https://ecampus.paris-saclay.fr/ . The maximal grade each exercice can get is 20: 5 points are given for using a correct coding style (tested by `pylint` with the custom `.pylintrc` from https://www.imo.universite-paris-saclay.fr/~schwartz/M398/pylintrc) and 15 for passing numerical tests (the examples from 2020-2021 appear in the file 'tests.py`). The results are stored in a pandas DataFrame exported to a csv file in the end.

**Attention:** This grader does not run submissions in a sandbox and is prone to «many» attacks )chain supply, code injection, stack overflow and more). One should really use it with great caution (and maybe sun it inside a sandbox to avoid damage).
