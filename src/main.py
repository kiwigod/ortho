import numpy as np
from time import time
from sys import argv
from fd.dir import Dir
from configuration import Configuration as C
from model.exercise import Exercise


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
    files = []
    for d in dirs:
        for f in d.get_files_recursively([]):
            files.append(f.exec(Exercise))
    files = np.array(files)
    print("Parsing data took %f seconds" % (time()-_start))

    """Reduce data points"""


    """Train model"""


    """Assert functionality"""

