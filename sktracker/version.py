
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import subprocess

__all__ = ["__version__"]

version = '0.2.dev'

if 'dev' in version:
    try:
        git_revision = subprocess.getoutput("git rev-parse --short master")
        git_revision = "-r" + git_revision
    except:
        git_revision = ""
else:
    git_revision

__version__ = version + git_revision
