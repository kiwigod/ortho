from model.meta import Meta


class File:
    def __init__(self, rel_path: str):
        self.path: str = rel_path
        self.meta: Meta = Meta(rel_path)

    def exec(self, callback):
        """
        Keep file access in one location.
        Defeats the purpose of opening files in unexpected locations

        :param function callback:
        :return: return value of the callback
        """
        with open(self.path) as f:
            return callback(f, self.meta)

    def __str__(self):
        return "Path: %s\n\n"\
               "Meta\n"\
               "----\n"\
               "%s" % (self.path, self.meta.__str__())
