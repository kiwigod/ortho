import joblib as jl


class MlInterface:
    """
    Reduce the functionality of the machine learning model.
    This in turn gives a clearer overview of what
    is possible with the model without looking for documentation
    """
    def __init__(self, clf):
        self.clf = clf

    def train(self, x, y):
        """
        Train the model using a combination
        of the given data and indicator

        :param list x: data
        :param list y: indicator
        """
        self.clf.fit(x, y)

    def predict(self, x):
        """
        Predict the indicator for the given data

        :param list x: data
        :return: Predicted values
        :rtype: list
        """
        return self.clf.predict(x)

    def dump(self, filename):
        """
        Save the trained model to a file

        :param str filename: path to save location
        """
        jl.dump(self.clf, filename)

    @classmethod
    def load(cls, filename):
        """
        Load the model as an instance of
        the implemented class

        :param str filename: path to model location
        :return: instance of implemented class
        """
        return cls(clf=jl.load(filename))
