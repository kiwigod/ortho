import os
from fd.file import File


class Dir:
    """
    Handle a directory's contents
    """
    def __init__(self, rel_path: str):
        """
        :param rel_path: relative path to the directory
        """
        self.path: str = rel_path
        self.dirs: [Dir] = self.__resolve_path(os.path.isdir, Dir)
        self.files: [File] = self.__resolve_path(lambda x: os.path.isfile(x) and x.endswith(".csv"), File)

    def get_files_recursively(self, all_files) -> list:
        """
        Retrieve all files from the parent and child directories

        :param list all_files: iterable; write the results
        :return: list of files from the current directory
        :rtype: list
        """
        if len(self.dirs) < 1:
            all_files.extend(self.files)
            return all_files

        all_files.extend(self.files)
        [d.get_files_recursively(all_files) for d in self.dirs]

        return all_files

    def __resolve_path(self, check, instance) -> list:
        """
        Resolve the contents of the given path

        :param callable check: Filter for which files to add
        :param callable instance: What instance must be created
        :return: list of instances
        """
        tmp = list()
        for f in os.listdir(self.path):
            _path = os.path.join(self.path, f)

            if check(_path):
                tmp.append(instance(_path))
        return tmp

    def __str__(self):
        res = ""
        _dirs = [x.path for x in self.dirs]
        _files = [x.path for x in self.files]

        if len(_dirs) > 0:
            res += "Directories\n"\
                   "-----------\n"
            for x in _dirs:
                res += x + "\n"
            res += "\n"

        if len(_files) > 0:
            res += "Files\n"\
                   "-----\n"
            for x in _files:
                res += x + "\n"

        return res
