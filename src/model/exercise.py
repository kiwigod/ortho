import _io
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

    def reduce_data(self, with_indicator: bool):
        """
        Reduce the data to the number of specified points

        :param bool with_indicator: return a list with true values
            alongside the requested points
        :return: data which can be used to train the model
        :rtype: np.ndarray|tupel
        """
        points = C.get("data_points")
        interval = int(len(self.nd) / points)
        data = np.ndarray(shape=(points, self.nd.shape[1]))
        [np.append(data, self.nd[i]) for i in range(0, len(self.nd), interval)]
        if with_indicator:
            indicator = [self.meta.cat] * points
            return data, indicator
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
        combination = C.get("exercise_combinations")
        if not combination:
            raise ExerciseCombinationNotSet("No exercise combination is set in your configuration file")
