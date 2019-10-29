from time import time
from sys import argv
from fd.dir import Dir
from exceptions import *
from configuration import Configuration as C
from model.exercise import Exercise, Statistics


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
            value = exercises.get(key)
            if value is None:
                exercises[key] = [f.exec(Exercise)]
            else:
                exercises[key].append(f.exec(Exercise))
    print("Parsing data took %f seconds" % (time()-_start))

    """Reduce data points"""
    for cat_pat, e in exercises:
        s = Statistics(e)
        combinations = s.calculate_combinations()

    """Train model"""


    """Assert functionality"""

