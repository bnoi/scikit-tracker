
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


"""Test dataset and fake auto generated trajectories.

When data function end with _temp. The file is being copied to a temporary
directory before its path is returned.
"""

import os
import tempfile
import shutil
import pandas as pd
import sys

from ..io.utils import load_img_list

data_path = os.path.dirname(os.path.realpath(__file__))

# Trajectories generator

from .trajectories_generator import directed_trajectories_generator
from .trajectories_generator import brownian_trajectories_generator


__all__ = ['directed_trajectories_generator',
           'brownian_trajectories_generator',
           'CZT_peaks',
           'sample_ome',
           'tubhiswt_4D',
           'stack_list_dir',
           'stack_list',
           'TZ_nucleus', 'TC_BF_cells',
           'metadata_json',
           'sample_h5',
           'sample_h5_temp',
           'brownian_trajs_df',
           'directed_motion_trajs_df',
           'trackmate_xml_temp',
           'trackmate_xml',
           'with_gaps_df']

# Image files


def CZT_peaks():
    """OME Tiff with fluo spots and CTZ dimensions.
    """
    return os.path.join(data_path, "CZT_peaks.ome.tif")


def CZT_peaks_temp():
    """
    """
    d = tempfile.gettempdir()
    f_ori = CZT_peaks()
    f_dest = os.path.join(d, "CZT_peaks.ome.tif")
    shutil.copy(f_ori, f_dest)
    return f_dest


def sample_ome():
    """OME Tiff with fluo spots and cells in BF and CTZ dimensions.
    """
    return os.path.join(data_path, "sample.ome.tif")


def tubhiswt_4D():
    """OME XML file from OME sample dataset.
    """
    return os.path.join(data_path, "tubhiswt-4D.ome.xml")


def stack_list_dir():
    """
    """
    return os.path.join(data_path, "stack_list")


def stack_list():
    """
    """
    dirname = stack_list_dir()
    file_list = load_img_list(dirname)
    return file_list


def TZ_nucleus():
    """
    """
    return os.path.join(data_path, "TZ_nucleus.ome.tif")


def TC_BF_cells():
    """
    """
    return os.path.join(data_path, "TC_BF_cells.ome.tif")

# JSON files


def metadata_json():
    """
    """
    return os.path.join(data_path, "metadata.json")


# HDF5 files
def nuclei_h5():
    stk_list = stack_list_dir()
    return os.path.join(data_path, stk_list, "Stack-1.h5")


def nuclei_h5_temp():
    """
    """
    d = tempfile.gettempdir()
    f_ori = nuclei_h5()
    f_dest = os.path.join(d, "nuclei.h5")
    shutil.copy(f_ori, f_dest)
    return f_dest


def sample_h5():
    """
    """
    if sys.version_info[0] < 3:
        return os.path.join(data_path, "sample_py2.h5")
    return os.path.join(data_path, "sample.h5")


def sample_h5_temp():
    """
    """
    d = tempfile.gettempdir()
    f_ori = sample_h5()
    f_dest = os.path.join(d, "sample.h5")
    shutil.copy(f_ori, f_dest)
    return f_dest


def brownian_trajs_df():
    """
    """
    store_path = os.path.join(data_path, "brownian_trajectories.h5")
    with pd.get_store(store_path) as store:
        trajs = store['trajs']
    return trajs


def directed_motion_trajs_df():
    """
    """
    store_path = os.path.join(data_path, "directed_motion_trajectories.h5")
    with pd.get_store(store_path) as store:
        trajs = store['trajs']
    return trajs


def with_gaps_df():
    """
    """
    with pd.get_store(os.path.join(data_path, "with_gaps.h5")) as store:
        trajs = store['trajs']
    return trajs


# XML files
def trackmate_xml():
    return os.path.join(data_path, "trackmate_example.xml")


def trackmate_xml_temp():
    """
    """
    d = tempfile.gettempdir()
    f_ori = os.path.join(data_path, "trackmate_example.xml")
    f_dest = os.path.join(d, "trackmate_example.xml")
    shutil.copy(f_ori, f_dest)
    return f_dest
