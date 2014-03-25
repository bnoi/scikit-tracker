import os
from ..io.utils import load_img_list

data_path = os.path.dirname(os.path.realpath(__file__))

def CZT_peaks():
    return os.path.join(data_path, "CZT_peaks.ome.tif")

def sample_ome():
    return os.path.join(data_path, "sample.ome.tif")

def tubhiswt_4D():
    return os.path.join(data_path, "tubhiswt-4D.ome.xml")

def metadata_json():
    return os.path.join(data_path, "metadata.json")

def sample_h5():
    return os.path.join(data_path, "sample_original.h5")

def stack_list_dir():
    return os.path.join(data_path, "stack_list")

def stack_list():
    dirname = stack_list_dir()
    file_list = load_img_list(dirname)
    return file_list

def TZ_nucleus():
    return os.path.join(data_path, "TZ_nucleus.ome.tif")

def TC_BF_cells():
    return os.path.join(data_path, "TC_BF_cells.ome.tif")
