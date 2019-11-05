import re


class Meta:
    def __init__(self, rel_path: str):
        self.cat: int = self.__parse_cat(rel_path)
        self.pat: int = self.__parse_pat(rel_path)
        self.ex: str = self.__parse_exercise(rel_path)

    def __parse_cat(self, text: str) -> int:
        return int(re.findall(r'category_(\d+)', text, re.IGNORECASE)[0])

    def __parse_pat(self, text: str) -> int:
        return int(re.findall(r'/(\d+)/', text, re.IGNORECASE)[0])

    def __parse_exercise(self, text: str) -> str:
        return str(re.findall(r'/(\w+)\d.csv', text, re.IGNORECASE)[0])

    def __str__(self):
        return "category: %i\n"\
               "patient:  %i\n"\
               "exercise: %s" % (self.cat, self.pat, self.ex)


class Filter:
    def __init__(self, **kwargs):
        self.cat = kwargs.get('cat')
        self.pat = kwargs.get('pat')
        self.ex = kwargs.get('ex')
        self.compiled = []

    def compile(self):
        """
        Create the filter attributes dynamically
        """
        self.compiled = []
        if self.cat is not None:
            self.compiled.append(lambda f: f.meta.cat == self.cat)
        if self.pat is not None:
            self.compiled.append(lambda f: f.meta.pat == self.pat)
        if self.ex is not None:
            self.compiled.append(lambda f: f.meta.ex == self.ex)
