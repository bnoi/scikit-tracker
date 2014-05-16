# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import warnings

from setuptools import find_packages
from setuptools import setup
from setuptools import Extension

# Get version number
import sys
sys.path.append('.')
import sktracker

# Fill project desciption fields
DISTNAME = 'scikit-tracker'
DESCRIPTION = 'Object detection and tracking for cell biology'
LONG_DESCRIPTION = open('README.md').read()
MAINTAINER = 'Guillaume Gay and Hadrien Mary'
MAINTAINER_EMAIL = 'gllm.gay@gmail.com'
URL = 'http://bnoi.github.io/scikit-tracker'
LICENSE = 'BSD 3-Clause'
DOWNLOAD_URL = 'https://github.com/bnoi/scikit-tracker'
VERSION = sktracker.__version__
PYTHON_VERSION = (3, 3)
DEPENDENCIES = ["numpy >= 1.8",
                "scipy >= 0.12",
                "pandas >= 0.13",
                "scikit-image >= 0.9",
                "scikit-learn >= 0.13",
                ]

if VERSION.endswith('dev'):
    DEPENDENCIES += ["nose >= 1.3",
                     "sphinx >= 1.2",
                     "coverage >= 3.7"
                     ]

# Try to use Cython to compile .pyx files.
# If Cython it not available then try to compile .c related files.
# So be sure to always have the .c version for each .pyx files.
# You can generate .c files with python setup.py build_ext --inplace
try:
    import numpy as np
except ImportError as e:
    raise ImportError("Numpy is needed to compile .pyx extensions. Use : pip install numpy")

try:
    from Cython.Distutils import build_ext
except ImportError as e:
    from setuptools.command.build_ext import build_ext
    warnings.warn("Cython is not present. .pyx extensions will be build against .c files.")

extensions = [Extension("sktracker.tracker.lapjv._lapjv",
                        ["sktracker/tracker/lapjv/_lapjv.pyx"],
                        include_dirs=[np.get_include()]),

              Extension("sktracker.io._tifffile",
                        ["sktracker/io/_tifffile.c"],
                        include_dirs=[np.get_include()]),
              ]

if __name__ == "__main__":

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

        packages=find_packages(),
        package_data={
            '': ['data/*.h5', 'data/*.xml', 'data/*.tif', 'data/stack_list/*.tif'],
        },

        tests_require='nose',
        test_suite='nose.collector',

        # Should DEPENDENCIES need to be included or let the user install them himself ?
        install_requires=[],
        # install_requires=DEPENDENCIES,
        setup_requires=['numpy'],

        cmdclass={"build_ext": build_ext},
        ext_modules=extensions,
    )
