#!/usr/bin/python
"""
Convert the specified patients in the current dir
ex. pat_conv 1 2 3 /home/yuqi/out
    -> Pick the given patients
    -> Create isolated env for conversion
    -> Store converted patients in out (out/pat/file)
"""


import os
from sys import argv
from shutil import copytree, rmtree


print("!!! Make sure the current directory contains the matlab script")
input("Press enter to continue...")


if not os.path.isdir(argv[-1]):
    print("%s is non existant; Exiting..." % argv[-1])
    exit(1)

out = argv[-1]
_pat = argv[1:-1]


dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d) and d in _pat]
parent = os.path.join(os.getcwd(), 'tmp')

for d in dirs:
    os.mkdir(parent)
    copytree(d, os.path.join(parent, d))
    # os.system('matlab -nojvm -r process_patient "%s %s"' % (parent, out))
    print('matlab -nojvm -r process_patient "%s %s"' % (parent, out))
    rmtree(parent)

print("Done~!")
exit(0)
