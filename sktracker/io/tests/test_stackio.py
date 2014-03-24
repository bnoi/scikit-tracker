from nose.tools import assert_raises

from sktracker import data
from sktracker.io import StackIO

# from nose import with_setup

# def open_tubhiswt_4D_ome_xml():
#     fname = "tubhiswt-4D.ome.xml"
#     f = open(os.path.join(current_dir, fname))
#     global xml_str
#     xml_str = f.read()
#     f.close()
#     return xml_str

# def xml_str_clean():
#     xml_str = None

# @with_setup(setup=open_tubhiswt_4D_ome_xml, teardown=xml_str_clean)
# def test_ome_loading():

#     m = OMEModel(xml_str)
#     del m

def test_stackio_from_tif_file():

    st = StackIO.from_tif_file(data.CZT_peaks())

    # Test metadata
