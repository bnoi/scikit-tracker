Installation
=============

Dependencies
------------

``sktracker`` depends on the following packages :

- Python >= 2.7 and >= 3.3
- numpy >= 1.8
- scipy >= 0.12
- pandas >= 0.13
- scikit-image >= 0.9
- scikit-learn >= 0.13
- matplotlib >= 1.3

**Optional**

- PyQt4

**For developers**

- nose >= 1.3
- sphinx >= 1.2
- coverage >= 3.7

From PyPI
---------

Available at https://pypi.python.org/pypi/scikit-tracker.

.. code-block:: sh

  $ pip install -U scikit-tracker

Installation from source (Github repo)
--------------------------------------

Here you will see how to install the last ``sktracker`` version.

One command line
~~~~~~~~~~~~~~~~

.. code-block:: sh

    $ pip install -e git+https://github.com/bnoi/scikit-tracker.git#egg=master

Clone and install
~~~~~~~~~~~~~~~~~

Obtain the source from the git repository at `https://github.com/bnoi/scikit-tracker
<https://github.com/bnoi/scikit-tracker>`_ by running :

.. code-block:: sh

  $ git clone https://github.com/bnoi/scikit-tracker.git

``sktracker`` can be installed globally using :

.. code-block:: sh

  $ python setup.py install
