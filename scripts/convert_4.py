#!/usr/bin/python
"""
Convert category 4 data to the expected format
ex. convert_4 /home/yuqi/in .DAT /home/yuqi/out
    -> Loop through directory
    -> Look for .DAT files
    -> Copy the detected files to out dir (out/pat/file.txt)
Author: Arjun Sardjoe Missier
"""

import os
import re
from sys import argv
from shutil import copyfile


def walk_dir(dir: str, ext: str, skip_org=True) -> list:
    """
    Walk through the given directory and look
    for the given extension

    :param str dir: Directory to look in
    :param str ext: File extension to look for
    :param bool skip_org: Skip original files?
    :return: Path to the files and the warning occured
    :rtype: tuple
    """
    paths = list()
    warnings = list()
    
    for fd in os.listdir(dir):
        _path = os.path.join(dir, fd)
        if os.path.isdir(_path):
            _data, _warnings = walk_dir(_path, ext)
            paths.extend(_data)
            warnings.extend(_warnings)

        if fd.endswith(ext) and os.path.isfile(_path):
            if skip_org and 'org' in fd:
                warnings.append(str("Skipping %s; Convert manually if needed" % _path))
                continue
            paths.append(_path)
    
    return paths, warnings


def touch_dir(path: str):
    """
    Create directory if not exist

    :param str path: path to directory
    """
    if not os.path.exists(path):
        os.makedirs(path)  # mkdir -p <path>


if len(argv) < 4:
    """
    Print usage when the number 
    of arguments do not match up
    """
    print("Usage: %s <path to cat 4> <.ext> <out> [verbosity toggle (0-1)]" % argv[0])
    exit(0)


# intialize command line parameters
verbose = argv[4] == '1' if 4 < len(argv) else False

# fix file extension
ext = argv[2]
if ext[0] != '.':
    ext = '.' + ext

_in = argv[1]
out = argv[3]


# retrieve files to process
data, warnings = walk_dir(_in, ext)

for f in data:
    # generate metadata
    cat = re.findall(r'category_(\d+)', f, re.IGNORECASE)[0]
    ex = re.findall(r'([a-zA-Z]+.)\.' + ext[1:], f, re.IGNORECASE)[0]
    pat = re.findall(r'\/(\d+)\/', f)[0]

    _parent = os.path.join(out, pat)
    touch_dir(_parent)
    _out = os.path.join(_parent, ex + '.txt')
    if verbose:
        print("Copying %s -> %s" % (f, _out))

    copyfile(f, _out)

print("--- The following warning occured during execution ---")
[print(w) for w in warnings]

print("Done~!")
exit(0)
