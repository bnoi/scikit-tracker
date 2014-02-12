import os
import sys
import re
import setuptools
from numpy.distutils.core import setup
from distutils.command.build_py import build_py

from sktracker import __version__

DISTNAME            = 'scikit-tracker'
DESCRIPTION         = 'Object detection and tracking for cell biology'
LONG_DESCRIPTION    = open('README.md').read()
MAINTAINER          = 'Guillaume Gay and Hadrien Mary'
MAINTAINER_EMAIL    = 'gllm.gay@gmail.com'
URL                 = 'http://bnoi.github.io/scikit-tracker'
LICENSE             = 'BSD 3-Clause'
DOWNLOAD_URL        = 'https://github.com/bnoi/scikit-tracker'
VERSION             = "0.1-dev"
PYTHON_VERSION      = (3, 3)
DEPENDENCIES        =  {
                        'numpy': (1, 8),
                        'scipy': (0, 12),
                        'pandas': (0, 13),
                        'skimage': (0, 9),
                        'sklearn': (0, 13),
                      }

# Only require Cython if we have a developer checkout
if VERSION.endswith('dev'):
    DEPENDENCIES['nose'] = (1, 3)
    DEPENDENCIES['sphinx'] = (1, 2)

def write_version_py(filename='sktracker/version.py'):
    template = """# This file is generated from the sktracker setup.py
__version__ = '%s'
"""

    vfile = open(os.path.join(os.path.dirname(__file__),
                              filename), 'w')

    try:
        vfile.write(template % VERSION)
    finally:
        vfile.close()

def get_package_version(package):
    version = []
    for version_attr in ('version', 'VERSION', '__version__'):
        if hasattr(package, version_attr) \
                and isinstance(getattr(package, version_attr), str):
            version_info = getattr(package, version_attr, '')
            for part in re.split('\D+', version_info):
                try:
                    version.append(int(part))
                except ValueError:
                    pass
    return tuple(version)

def check_requirements():
    if sys.version_info < PYTHON_VERSION:
        raise SystemExit('You need Python version %d.%d or later.' \
                         % PYTHON_VERSION)

    for package_name, min_version in DEPENDENCIES.items():
        dep_error = False
        try:
            package = __import__(package_name)
        except ImportError:
            dep_error = True
        else:
            package_version = get_package_version(package)
            if min_version > package_version:
                dep_error = True

        if dep_error:
            raise ImportError('You need `%s` version %d.%d or later.' \
                              % ((package_name, ) + min_version))


if __name__ == "__main__":

    check_requirements()

    write_version_py()

    setup(
        name=DISTNAME,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        url=URL,
        license=LICENSE,
        download_url=DOWNLOAD_URL,
        version=VERSION,

        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS',
        ],

        packages=setuptools.find_packages(exclude=['doc']),
        include_package_data=True,
        zip_safe=False, # the package can run out of an .egg file

        entry_points={
            'console_scripts': [],
        },

        cmdclass={'build_py': build_py},
    )
