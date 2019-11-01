from sklearn.linear_model.logistic import LogisticRegression as SKLR
from ml.mlinterface import MlInterface


class LogisticRegression(MlInterface):
    def __init__(self, clf=None, **kwargs):
        if clf is None:
            clf = SKLR(**kwargs)
        super().__init__(clf)
