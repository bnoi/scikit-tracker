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
