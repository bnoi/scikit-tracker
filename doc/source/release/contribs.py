
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


#!/usr/bin/env python
import subprocess
import sys
import string
import shlex

if len(sys.argv) != 2:
    print("Usage: ./contributors.py tag-of-previous-release")
    sys.exit(-1)

tag = sys.argv[1]


def call(cmd):
    return subprocess.check_output(shlex.split(cmd)).decode('utf-8').split('\n')

tag_date = call("git show --format='%%ci' %s" % tag)[0]
print("Release %s was on %s" % (tag, tag_date))

merges = call("git log --since='%s' --merges --format='>>>%%B' --reverse" % tag_date)
merges = [m for m in merges if m.strip()]
merges = '\n'.join(merges).split('>>>')
merges = [m.split('\n')[:2] for m in merges]
merges = [m for m in merges if len(m) == 2 and m[1].strip()]

print("\nIt contained the following %d merges:" % len(merges))
print
for (merge, message) in merges:
    if merge.startswith('Merge pull request #'):
        PR = ' (%s)' % merge.split()[3]
    else:
        PR = ''

    print('- ' + message + PR)


print("""\nThis release was made possible by the collaborative efforts of many
contributors, both new and old.  They are listed in alphabetical order by
surname:\n""")

authors = call("git log --since='%s' --format=%%aN" % tag_date)
authors = [a.strip() for a in authors if a.strip()]


def key(author):
    author = [v for v in author.split() if v[0] in string.ascii_letters]
    return author[-1]

authors = sorted(set(authors), key=key)

for a in authors:
    print('-', a)
