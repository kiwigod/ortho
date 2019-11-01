from time import time
from configuration import Configuration as C
from multiprocessing import Process
from multiprocessing import Manager as MPManager
from process.exceptions import *


class Manager:
    """
    Helper class for processes
    """
    manager: MPManager = MPManager()
    instances: [Process] = []

    @staticmethod
    def shared_dict() -> dict:
        """
        Generate a dict which can be used across multiple processes

        :return: dict which can be shared across multiple processes
        :rtype: dict
        """
        return Manager.manager.dict()

    @staticmethod
    def shared_list() -> list:
        """
        Generate a lists which can be used across multiple processes

        :return: list which can be shared across multiple processes
        :rtype: list
        """
        return Manager.manager.list()

    @staticmethod
    def create_process(target, args=None, start=True, is_daemon=True) -> int:
        """
        Create a process targeting the given function

        :param function target: Callback to the function which the process needs to complete
        :param tuple args: Optional; Arguments to feed the callback
        :param bool start: Optional; Instantly start the process after creation
        :param bool is_daemon: Optional; Flag the process as a daemon
        :raise ExceedMaxProcessesError: Too many processes have been spawned
        :return: index of the process in the instances list
        :rtype: int
        """
        if len(Manager.instances) > C.get("max_processes"):
            raise ExceedMaxProcessesError

        p = Process(target=target, args=args)
        p.daemon = is_daemon  # a daemon cannot spawn child processes
        if start:
            p.start()
        Manager.instances.append(p)
        return len(Manager.instances)-1

    @staticmethod
    def start(index) -> int:
        """
        Start a generated process

        :param int index: Index of the process to start
        :raise ProcessAlreadyRunningError: Requested process is already running
        :return: PID of the started process
        :rtype: int
        """
        if Manager.instances[index].is_alive():
            raise ProcessAlreadyRunningError

        Manager.instances[index].start()
        return Manager.instances[index].pid

    @staticmethod
    def join(index, close=True):
        """
        Join a running process

        :param int index: Index of the process to join
        :param bool close: Close the joined process
        :raise ProcessNotRunningError: Requested process isn't running
        """
        if not Manager.instances[index].is_alive():
            raise ProcessNotRunningError

        Manager.instances[index].join()
        if close:
            Manager.instances[index].close()
        del (Manager.instances[index])

    @staticmethod
    def join_all():
        """
        Join all known process instances
        """
        _start = time()
        for p in Manager.instances:
            p.join()
            p.close()
        print("Joined jobs")
        print("Completing and closing open jobs took %f seconds" % (time() - _start))
        Manager.instances = []

    @staticmethod
    def kill_all():
        """
        !WARNING! This force kills all processes without waiting for their results
        Kill all known process instances
        Children of the main process will become orphaned
        """
        for p in Manager.instances:
            p.kill()
        Manager.instances = []  # reset instances
