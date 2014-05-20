
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


"""Script to commit the doc build outputs into the github-pages repo.

In practice, you should use either actual clean tags from a current build or
something like 'current' as a stable URL for the mest current version of the """

# Imports
import os
import re
import shutil
import sys
from os import chdir as cd

from subprocess import Popen, PIPE, CalledProcessError, check_call

pages_dir = 'gh-pages'
html_dir = 'build/html'
pdf_dir = 'build/latex'
pages_repo = 'git@github.com:bnoi/scikit-tracker.git'


def sh(cmd):
    """Execute command in a subshell, return status code."""
    return check_call(cmd, shell=True)


def sh2(cmd):
    """Execute command in a subshell, return stdout.

    Stderr is unbuffered from the subshell.x"""
    p = Popen(cmd, stdout=PIPE, shell=True)
    out = p.communicate()[0]
    retcode = p.returncode
    if retcode:
        print(out.rstrip())
        raise CalledProcessError(retcode, cmd)
    else:
        return out.rstrip()


def sh3(cmd):
    """Execute command in a subshell, return stdout, stderr

    If anything appears in stderr, print it out to sys.stderr"""
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p.communicate()
    retcode = p.returncode
    if retcode:
        raise CalledProcessError(retcode, cmd)
    else:
        return out.rstrip(), err.rstrip()


def init_repo(path):
    """clone the gh-pages repo if we haven't already."""
    sh("git clone %s %s" % (pages_repo, path))
    here = os.getcwd()
    cd(path)
    sh('git checkout gh-pages')
    cd(here)

# Script starts

if __name__ == '__main__':

    sys.path.append('..')
    import sktracker
    version = sktracker.__version__

    if "dev" in version:
        tag = "dev"
    else:
        tag = version

    startdir = os.getcwd()
    if not os.path.exists(pages_dir):
        init_repo(pages_dir)
    else:
        cd(pages_dir)
        sh('git checkout gh-pages')
        sh('git pull')
        cd(startdir)

    dest = os.path.join(pages_dir, tag)

    # This is pretty unforgiving: we unconditionally nuke the destination
    # directory, and then copy the html tree in there
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(html_dir, dest)

    try:
        cd(pages_dir)
        status = sh2('git status | head -1').decode("utf-8")
        branch = re.match('\# On branch (.*)$', status).group(1)
        if branch != 'gh-pages':
            e = 'On %r, git branch is %r, MUST be "gh-pages"' % (pages_dir,
                                                                 branch)
            raise RuntimeError(e)
        sh("touch .nojekyll")

        if 'dev' not in tag:
            sh('rm -f stable')
            sh('ln -s %s stable' % tag)

        sh('git add . --all')
        sh2('git commit -am "Updated doc release: {}" --allow-empty'.format(version))

        print('Most recent commit:')
        sys.stdout.flush()
        sh('git --no-pager log --oneline HEAD~1..')
    finally:
        cd(startdir)

    print('')
    print('Now verify the build in: %r' % dest)
    print("If everything looks good, run 'git push' inside doc/gh-pages.")
