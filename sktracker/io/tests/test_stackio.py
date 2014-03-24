import os

from nose import with_setup

data_dir = os.path.dirname(os.path.realpath(__file__))

def open_tubhiswt_4D_ome_xml():
    fname = "tubhiswt-4D.ome.xml"
    f = open(os.path.join(current_dir, fname))
    global xml_str
    xml_str = f.read()
    f.close()
    return xml_str

def xml_str_clean():
    xml_str = None

# @with_setup(setup=open_tubhiswt_4D_ome_xml, teardown=xml_str_clean)
# def test_ome_loading():

#     m = OMEModel(xml_str)
#     del m
