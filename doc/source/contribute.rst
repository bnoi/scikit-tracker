Contribute to development
=========================

**scikit-tracker** is community driven which means that anyone can contribute. There is different
ways to help scikit-tracker development :

- report bugs to https://github.com/bnoi/scikit-tracker/issues
- write documentation (:ref:`use cases <use-cases>` are welcome !)
- open Pull Request on Github to fix, bugs or add new features

Active contributors can ask to become official member with write access to the github repository.

Development process
-------------------

Development workflow follows numpy guidelines available at
http://docs.scipy.org/doc/numpy/dev/gitwash/development_workflow.html.

Guidelines
----------

(*partially stolen from http://scikit-image.org/docs/dev/contribute.html*)

- All code should have tests (with `nose` module) in a module repository called ``tests``.
- All code should be documented, to the same standard as NumPy and SciPy.
- For new features, try to add example on docstring or in documentation (:ref:`basics` or :ref:`use-cases`).
- Heavy new algorithms should be described in a theoretically point of view in :ref:`theory`.

- After opening a new Pull Request Travis-CI will check that everything is fine. Don't forget to
  adapt ``travis.yml`` when it's appropriate.

Stylistic Guidelines
--------------------

- Set up your editor to remove trailing whitespace.
- Always check your code with a PEP8 checker (``pep8`` and/or ``pyflakes``)
- Use the following import conventions::

    import numpy as np
    import scipy as sp
    import pandas as pd
    import matplotlib.pyplot as plt

Test coverage
-------------

scikit-tracker use ``overage`` (``pip install coverage``)`to check code coverage during tests.
Ideally it should be always 100%. In fact coverage above 90% is fine.

To launch coverage got the scikit-tracker root::

    make coverage

Continous integration with Travis-CI
------------------------------------

Travis-CI (https://travis-ci.org/bnoi/scikit-tracker) build, installs, tests and check coverage each
time a commit is made or a pull request open on the github repository.

Optionally you can enable Travis-CI check for your own scikit-tracker fork:

- Go to Travis-CI and follow the Sign In link at the top
- Go to your profile page and switch on your ``scikit-tracker`` fork
- Thus, as soon as you push your code to your fork, it will trigger Travis-CI, and you will receive
  an email notification when the process is done.

Tips for developers
-------------------

A Makefile at the root of the repository provides several commands:

- ``init-submodule`` and ``update-submodule``: required to build documentation
- ``clean``: remove temporary Python files
- ``flake8``: check PEP8 (need ``pip install flake8``)
- ``test``: run ``nose`` tests
- ``coverage``: run ``nose`` tests with coverage
- ``doc``: build documentation with Sphinx
- ``doc-execute-notebook``: execute notebooks and then build documentation with Sphinx
- ``push-doc``: push doc to scikit-tracker.org (need write access to github repository)
- ``open-doc``: open locally built doc in default browser
