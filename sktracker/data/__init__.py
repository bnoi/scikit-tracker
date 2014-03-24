import os

data_path = os.path.dirname(os.path.realpath(__file__))

def CZT_peaks():
    return os.path.join(data_path, "CZT_peaks.ome.tif")

def sample():
    return os.path.join(data_path, "sample.ome.tif")

def tubhiswt_4D():
    return os.path.join(data_path, "tubhiswt-4D.ome.xml")

def metadata_json():
    return os.path.join(data_path, "metadata.json")
