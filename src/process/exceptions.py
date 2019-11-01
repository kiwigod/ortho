class ExceedMaxProcessesError(Exception):
    """Raised when too many processes are spawned"""
    pass


class ProcessAlreadyRunningError(Exception):
    """
    Raised when a process is requested to start,
    but is already running
    """
    pass


class ProcessNotRunningError(Exception):
    """
    Raised when join or kill is called on a process,
    but the process has not been started yet
    """
    pass
