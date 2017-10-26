#!/usr/bin/env python
"""gcc.py is a wrapper for the Cray compiler,
  converting/removing incompatible gcc args.   """

import sys
from subprocess import call
from glob import glob

args2change = {
        '-fno-strict-aliasing':'',
        '-Wall':'',
        '-Wstrict-prototypes':'',
        '-DNDEBUG':'',
        '-UNDEBUG':''
        }
fragile_files = []

optimise = None  # optimisation level 0/1/2/3
debug = False    # use -g or not
fragile = False  # use special flags for current file?

# process arguments
args = []
for arg in sys.argv[1:]:
    arg = arg.strip()
    if arg.startswith('-O'):
        level = int(arg.replace('-O',''))
        if not optimise or level > optimise:
            optimise = level
    elif arg == '-g':
        debug = True
    elif arg in args2change:
        if args2change[arg]:
            args.append(args2change[arg])
    else:
        if arg in fragile_files:
            fragile = True
        args.append(arg)

# set default optimisation level and flags
if fragile:
    optimise = min(2, optimise)
    flags = []
else:
    optimise = max(3, optimise)
    flags = ['-funroll-loops', '-mavx2']

# add optimisation level to flags
if optimise is not None:
    flags.insert(0, '-O{0}'.format(optimise))
# make sure -g is always the _first_ flag, so it doesn't mess e.g. with the
# optimisation level
if debug:
    flags.insert(0, '-g')

# construct and execute the compile command
cmd = 'cc {0} {1}'.format(' '.join(flags), ' '.join(args))
print(cmd)
call(cmd, shell=True)
