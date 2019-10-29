from time import time
from sys import argv
from fd.dir import Dir
from exceptions import *
from configuration import Configuration as C
from model.exercise import Exercise, Statistics
from model.meta import Filter


def filter_files(filter: Filter, files: [Exercise]):
    for fil in filter.compiled:
        files = [f for f in files if fil(f)]
    return files


if __name__ == '__main__':
    """Create configuration"""
    try:
        argv[1]
    except IndexError:
        print("Usage:", argv[0], "/path/to/config")
        exit(1)
    C.setup(argv[1])

    """Parse data"""
    _start = time()
    dirs = [
        Dir("data/Category_1"),
        Dir("data/Category_2"),
        Dir("data/Category_3")
    ]
    exercises = {}
    for d in dirs:
        for f in d.get_files_recursively([]):
            key = "%s_%s" % (f.meta.cat, f.meta.pat)
            if exercises.get(key) is None:
                exercises[key] = [f.exec(Exercise)]
            else:
                exercises[key].append(f.exec(Exercise))
    print(exercises)
    print("Parsing data took %f seconds" % (time()-_start))

    """Reduce data points"""
    for cat_pat, e in exercises.items():
        s = Statistics(e)
        try:
            combinations = s.calculate_combinations()
        except NotAllExpectedExercisesPerformedError:
            print("%s has not performed all exercises; Skipping" % cat_pat)
            continue

    """Train model"""


    """Assert functionality"""

