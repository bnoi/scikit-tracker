Scikit-tracker's documentation
==============================

.. raw:: html

   <p style="height:22px">
     <a href="https://travis-ci.org/bnoi/scikit-tracker" >
       <img src="https://travis-ci.org/bnoi/scikit-tracker.png?branch=master"/>
     </a>
     <a href="http://dx.doi.org/10.5281/zenodo.10078" >
       <img src="https://zenodo.org/badge/doi/10.5281/zenodo.10078.png"/>
     </a>
   </p>

- **Version** : |version| |rev_date|
- **Source code** : https://github.com/bnoi/scikit-tracker
- **Issues, ideas and discussions** : https://github.com/bnoi/scikit-tracker/issues

**scikit-tracker** aims to be a robust Python library to work with cell
biology microscopy images. `OME XML and OME Tiff`_ are supported to
handle input/output to the lib. The two main goals of the library is to
implement **detection** and **tracking** algorithms relevant to analyse
biological microscopy dataset.

Several algorithms are featured and it is planned to add others:

-  **Gaussian peak detection** by deflation loop : `Segré et al. Nature
   Methods (2008)`_

- **Cell boundary detection** with bright field depth fitting : `Julou, T., PNAS, (2013)`_

-  **Cell nucleus segmentation** : by Guillaume Gay

-  **Lap Tracker**, a robust single-particle tracking : `K. Jaqaman and G.
   Danuser, Nature Methods, 2008`_. The version implemented in
   **scikit-tracker** is a slightly modified version from the original
   to allow easy, flexible and yet powerfull parameters adjustements
   with custom cost function.

**scikit-tracker** provides several intuitive graphical interfaces to semi-manually modify detected objects and trajectories (thanks to Qt4).

.. note::
    **scikit-tracker** and ``sktracker`` refer to the same thing. However **scikit-tracker** may be used more as a project name while ``sktracker`` as a Python module.

.. _OME XML and OME Tiff: https://www.openmicroscopy.org/site/support/ome-model/ome-tiff/
.. _Segré et al. Nature Methods (2008): http://www.nature.com/nmeth/journal/v5/n8/full/nmeth.1233.html
.. _K. Jaqaman and G. Danuser, Nature Methods, 2008: http://www.nature.com/nmeth/journal/v5/n8/full/nmeth.1237.html
.. _Julou, T., PNAS, (2013): http://www.pnas.org/content/early/2013/07/10/1301428110

Table of content
----------------

.. toctree::
    :maxdepth: 3

    new

    theory
    install
    basics
    use_cases
    api/sktracker
    contribute
    cite
    license
