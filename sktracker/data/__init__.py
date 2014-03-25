"""Test dataset and fake auto generated trajectories.

When data function end with _temp. The file is being copied to a temporary
directory before its path is returned.
"""

import os
import tempfile
import shutil

from .trajectories_generator import trajectories_generator

from ..io.utils import load_img_list

data_path = os.path.dirname(os.path.realpath(__file__))

def CZT_peaks():
    """OME Tiff with fluo spots and CTZ dimensions.
    """
    return os.path.join(data_path, "CZT_peaks.ome.tif")

def sample_ome():
    """OME Tiff with fluo spots and cells in BF and CTZ dimensions.
    """
    return os.path.join(data_path, "sample.ome.tif")

def tubhiswt_4D():
    """OME XML file from OME sample dataset.
    """
    return os.path.join(data_path, "tubhiswt-4D.ome.xml")

def metadata_json():
    """
    """
    return os.path.join(data_path, "metadata.json")

def sample_h5():
    """
    """
    return os.path.join(data_path, "sample.h5")

def sample_h5_temp():
    """
    """
    d = tempfile.gettempdir()
    f_ori = os.path.join(data_path, "sample.h5")
    f_dest = os.path.join(d, "sample.h5")
    shutil.copy(f_ori, f_dest)
    return f_dest

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
