import re


class Meta:
    def __init__(self, rel_path: str):
        self.cat: int = self.__parse_cat(rel_path)
        self.pat: int = self.__parse_pat(rel_path)
        self.ex: str = self.__parse_exercise(rel_path)

    def __parse_cat(self, text: str):
        return int(re.findall(r'category_(\d+)', text, re.IGNORECASE)[0])

    def __parse_pat(self, text: str):
        return int(re.findall(r'/(\d+)/', text, re.IGNORECASE)[0])
        pass

    def __parse_exercise(self, text: str):
        return str(re.findall(r'/(\w+)\d.csv', text, re.IGNORECASE)[0])
