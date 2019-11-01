from time import time
from sys import argv
from sklearn.metrics import classification_report, accuracy_score
from fd.dir import Dir
from exceptions import NotAllExpectedExercisesPerformedError
from configuration import Configuration as C
from model.exercise import Exercise, Statistics
from ml.linear.logistic import LogisticRegression


def ex():
    exit()


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
    dirs = {
        1: Dir("data/Category_1"),
        2: Dir("data/Category_2"),
        3: Dir("data/Category_3"),
        4: Dir("data/Category_4")
    }
    dir_file_count = {1: None, 2: None, 3: None, 4: None}
    exercises = {}
    for cat, d in dirs.items():
        files = d.get_files_recursively([])
        dir_file_count[cat] = len(files)
        for f in files:
            key = "%s_%s" % (f.meta.cat, f.meta.pat)
            if exercises.get(key) is None:
                exercises[key] = [f.exec(Exercise)]
            else:
                exercises[key].append(f.exec(Exercise))
    print("Parsing data took %f seconds" % (time()-_start))

    """Determine test patients"""
    split = C.get('test_split')
    test_patients = list()
    test_patients_count = {1: 0, 2: 0, 3: 0, 4: 0}
    for cat_pat, e in exercises.items():
        _split = cat_pat.split('_', 1)
        cat = int(_split[0])

        needed = int(dir_file_count[cat] * (split/100))
        if test_patients_count[cat] >= needed:
            continue

        test_patients.append(cat_pat)
        test_patients_count[cat] += len(e)

    """Reduce data points"""
    data = list()
    test_data = list()
    indicator = list()
    test_indicator = list()
    for cat_pat, e in exercises.items():
        s = Statistics(e)
        try:
            combinations = s.calculate_combinations()
        except NotAllExpectedExercisesPerformedError:
            print("%s has not performed all expected exercises; Skipping" % cat_pat)
            continue

        for c in combinations:
            _tmp = []
            [_tmp.extend(ex.reduced) for ex in c]

            if cat_pat in test_patients:
                test_data.append(_tmp)
                test_indicator.append(c[0].meta.cat)
            else:
                data.append(_tmp)
                indicator.append(c[0].meta.cat)
    print(len(data), len(test_data))
    print(len(indicator), len(test_indicator))

    """Train model"""
    model = LogisticRegression(solver="lbfgs", multi_class="auto", max_iter=2000, n_jobs=-1, verbose=1)
    model.train(data, indicator)

    """Assert functionality"""
    test_pred = model.predict(test_data)
    print(classification_report(test_indicator, test_pred, digits=3))
    print(accuracy_score(test_indicator, test_pred, normalize=True, sample_weight=None))
