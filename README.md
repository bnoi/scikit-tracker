# THIS PROJECT IS NOW UNMAINTENED AND DEPRECATED

# Objects detection and robust tracking for cell biology

[![Build Status](https://travis-ci.org/bnoi/scikit-tracker.png?branch=master)](https://travis-ci.org/bnoi/scikit-tracker)
[![scikit-tracker DOI](https://zenodo.org/badge/doi/10.5281/zenodo.10078.png)](http://dx.doi.org/10.5281/zenodo.10078)

**scikit-tracker** aims to be a robust Python library to work with cell biology microscopy images. [OME XML and OME Tiff](https://www.openmicroscopy.org/site/support/ome-model/ome-tiff/) are supported to handle input/output to the lib. The two main goals of the library is to implement **detection** and **tracking** algorithms relevant to analyse biological microscopy dataset.

Several algorithms are featured and it is planned to add others:

- Gaussian peak detection by deflation loop : [Segré et al. Nature Methods (2008)](http://www.nature.com/nmeth/journal/v5/n8/full/nmeth.1233.html)

- Cell boundary detection with bright field depth fitting : [Julou, T., PNAS, (2013)](http://www.pnas.org/content/early/2013/07/10/1301428110)

- Cell nucleus segmentation : by Guillaume Gay

- Lap Tracker, a robust single-particle tracking : [K. Jaqaman and G. Danuser, Nature Methods, 2008](http://www.nature.com/nmeth/journal/v5/n8/full/nmeth.1237.html). The version implemented in **scikit-tracker** is a slightly modified version from the original to allow easy, flexible and yet powerfull parameters adjustements with custom cost function.

**scikit-tracker** provides several intuitive graphical interfaces to semi-manually modify detected objects and trajectories (thanks to Qt4).

## Documentation

Current stable version is v0.2.

- Stable version : http://scikit-tracker.org/stable
- Dev version : http://scikit-tracker.org/dev

## Dependencies

- Python >= 2.7 and >= 3.3
- numpy >= 1.8
- scipy >= 0.12
- pandas >= 0.13
- scikit-image >= 0.9
- scikit-learn >= 0.13
- matplotlib >= 1.3

### Optional

- PyQt4

### For developers

- nose >= 1.3
- sphinx >= 1.2
- coverage >= 3.7

## Installation

You can install scikit-tracker using pip:

    $ pip install scikit-tracker

Or by cloning this repo and using setup.py:

    $ git clone git@github.com:bnoi/scikit-tracker.git
    $ python setup.py install

## Authors

- Guillaume Gay : gllm.gay@gmail.com
- Hadrien Mary : hadrien.mary@gmail.com

## Licence

See [LICENSE](LICENSE).
