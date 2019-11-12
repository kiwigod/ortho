#!/usr/bin/python
"""
Verify category conversion (txt -> csv)
ex. cat_integrity /home/yuqi/conv /home/yuqi/raw
    -> Loop through converted
    -> Check for existance of counterpart raw file
Author: Arjun Sardjoe Missier
"""


import os
import re
from sys import argv


class Meta:
    """
    Class for data housing and comparison
    """
    def __init__(self, path: str):
        self.path = path
        self.cat = self.__parse_cat()
        self.pat = self.__parse_pat()
        self.ex  = self.__parse_ex()

    def __parse_cat(self):
        return re.findall(r'cat_(\d+)', self.path, re.IGNORECASE)[0]

    def __parse_ex(self):
        return re.findall(r'([a-zA-Z]+.)\.', self.path, re.IGNORECASE)[0]

    def __parse_pat(self):
        return re.findall(r'\/(\d+)\/', self.path)[0]

    def __eq__(self, other):
        return (
            self.cat == other.cat and
            self.pat == other.pat and
            self.ex  == other.ex)

    def __str__(self):
        return "path: %s\n"\
            "category: %s\n"\
            "patient: %s\n"\
            "exercise: %s" % (self.path, self.cat, self.pat, self.ex)


def walk_dir(dir: str, ext: str) -> list:
    """
    Walk through the given directory and look
    for the given extension

    :param str dir: Directory to look in
    :param str ext: File extension to look for
    :return: Path to the files
    :rtype: list
    """
    paths = list()

    for fd in os.listdir(dir):
        _path = os.path.join(dir, fd)
        if os.path.isdir(_path):
            paths.extend(walk_dir(_path, ext))

        if fd.endswith(ext) and os.path.isfile(_path):
            paths.append(_path)
    
    return paths


if len(argv) < 3:
    print("Usage: %s <conv dir> <raw dir>" % argv[0])
    exit(0)

conv = walk_dir(argv[1], '.csv')
conv_meta = [Meta(fd) for fd in conv]
raw = walk_dir(argv[2], '.txt')
raw_meta = [Meta(fd) for fd in raw]

patients = set()
for m in conv_meta:
    if m not in raw_meta:
        print("Warning: File with matching metadata has not been found in given raw path")
        print(m)
        patients.add(m.pat)

if len(patients) > 0:
    print("The following patients contain invalid data, and should be excluded")
    [print(p) for p in patients]
else:
    print("Category integrity asserterd")

print("Done~!")
exit(0)
