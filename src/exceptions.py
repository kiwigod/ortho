class ExerciseCombinationNotSetError(Exception):
    """
    Raised when no exercise combination is set in the config file
    """
    pass


class NotAllExpectedExercisesPerformedError(Exception):
    """
    Raised when the expected exercise combination is not achieved
    """
    pass
