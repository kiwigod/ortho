import _io
import math
import numpy as np
import itertools
from exceptions import *
from model.meta import Meta
from configuration import Configuration as C


class Exercise:
    def __init__(self, csv: _io.TextIOWrapper, meta: Meta):
        """
        :param _io.TextIOWrapper csv: csv file to parse
        :param Meta meta: Meta object associated with the exercise
        """
        self.nd: np.ndarray = self.__read_csv_numpy(csv)
        self.reduced = self.reduce_data()
        self.meta: Meta = meta

    def __read_csv_numpy(self, csv) -> np.ndarray:
        """
        Parse the given csv using numpy

        :param _io.TextIOWrapper csv: csv file to parse
        :return: numpy array with exercise data
        :rtype: numpy.ndarray
        """
        nd = np.genfromtxt(csv, delimiter=',')
        nd = np.delete(nd, [13, 14, 28, 29], axis=1)  # delete columns which are always 0
        return nd

    def reduce_data(self):
        """
        Reduce the data to the number of specified points

        :return: data which can be used to train the model
        :rtype: np.ndarray|tuple
        """
        points = C.get("data_points")
        interval = math.ceil(len(self.nd) / points)
        data = list()

        [data.extend(self.nd[i]) for i in range(0, len(self.nd), interval)]

        return data

    def __str__(self) -> str:
        """
        Override the str call

        :return: string representation of the ndarray
        """
        return str(self.nd[:3])


class Statistics:
    def __init__(self, exercises: [Exercise]):
        self.exercises = exercises

    def calculate_combinations(self) -> list:
        """
        Generate exercise combinations
        :return: list of exercise combinations
        """
        combination = C.get("exercise_combinations")
        if not combination:
            raise ExerciseCombinationNotSetError("No exercise combination is set in your configuration file")

        exercises = {}
        for c in combination:
            _exercises = [f for f in self.exercises if f.meta.ex == c]

            if len(_exercises) < 1:
                raise NotAllExpectedExercisesPerformedError("Patient %i in category %i "
                                                            "has not performed %s" %
                                                            (self.exercises[0].meta.pat, self.exercises[0].meta.cat, c))

            exercises[c] = _exercises

        # print(self.exercises[0].meta.cat, self.exercises[0].meta.pat)
        # [print(x, len(y)) for x, y in exercises.items()]
        # print(len(list(itertools.product(*exercises.values()))))

        # return list(itertools.product(*[exercises[c] for c in combination]))
        return list(itertools.product(*exercises.values()))
