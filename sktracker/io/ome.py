# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import sys
import io
import logging
import uuid
from xml.etree import cElementTree as ElementTree

import numpy as np
import pandas as pd

import tempfile


log = logging.getLogger(__name__)

__all__ = []

NAMESPACE_2012 = "http://www.openmicroscopy.org/Schemas/OME/2012-06"
NAMESPACE_2013 = "http://www.openmicroscopy.org/Schemas/OME/2013-06"


class OMEModel():
    """OMEModel allows OME xml manipulation in order to read and write OME
    metadata.

    Parameters
    ----------
    xml_str: str
        OME XML string

    """

    def __init__(self, xml_str):
        """Load OME XML string.
        """

        self.root = ElementTree.XML(xml_str)

        self.ns = NAMESPACE_2012
        self.img = self.root.find("{%s}Image" % self.ns)
        if not self.img:
            self.ns = NAMESPACE_2013
            self.img = self.root.find("{%s}Image" % self.ns)

        if not self.img:
            log.critical('OME XML does not contain Image tag.')
        else:
            self.pixels = self.img.find("{%s}Pixels" % self.ns)
            if not self.pixels:
                log.critical('OME XML Image tag does not contain Pixels tag.')

        try:
            self.planes = self.pixels.findall("{%s}Plane" % self.ns)
        except:
            log.error('OME model does not contain Plane tag')
            self.planes = None

    def df_planes(self, sup_cols=[]):
        """Get OME Plane tags as `pd.DataFrame`.

        Parameters
        ----------
        sup_cols: list
            Supplementaries columns to retrieve

        Returns
        -------
        df_planes: :class:`pd.DataFrame`
            Contains OME XML Plane informations

        """
        if self.planes:
            cols = ["TheC", "TheT", "TheZ"]
            cols += sup_cols

            def get_values(x):
                ret = []
                for tag in cols:
                    if tag in x.attrib.keys():
                        ret.append(x.attrib[tag])
                return ret

            values = list(map(get_values, self.planes))
            df_planes = pd.DataFrame(values, columns=cols).astype('float')
            df_planes = df_planes.set_index(["TheT", "TheC", "TheZ"])

            return df_planes

        else:
            return None

    def get_metadata(self):
        """Retrieve global metadata from OME.

        Notes
        -----
        If some metadata are missing (such as `z-size`), they are inferred from
        Plane tags.

        Returns
        -------
        metadata: dict
            Metadata from OME XML

        """

        if not self.img or not self.pixels:
            return {}

        md = {}

        img = self.root.find("{%s}Image" % self.ns)

        acq_date = img.find("{%s}AcquisitionDate" % self.ns)
        if acq_date is not None:
            md['AcquisitionDate'] = acq_date.text

        # Find x and y real dimensions
        if "PhysicalSizeX" in self.pixels.attrib.keys():
            x_size = float(self.pixels.attrib["PhysicalSizeX"])
            md['PhysicalSizeX'] = x_size
        if "PhysicalSizeY" in self.pixels.attrib.keys():
            y_size = float(self.pixels.attrib["PhysicalSizeY"])
            md['PhysicalSizeY'] = y_size
        if "PhysicalSizeZ" in self.pixels.attrib.keys():
            z_size = float(self.pixels.attrib["PhysicalSizeZ"])
            md['PhysicalSizeZ'] = z_size

        # Find dimension order
        if "DimensionOrder" in self.pixels.attrib.keys():
            md['DimensionOrder'] = self.pixels.attrib["DimensionOrder"]
            md['DimensionOrder'] = list(reversed(md['DimensionOrder']))

        if 'DimensionOrder' in md.keys():
            shape = []
            for d in md['DimensionOrder']:
                try:
                    s = self.pixels.attrib['Size' + d]
                    shape.append(int(s))
                except:
                    shape.append(1)
            md['Shape'] = tuple(shape)

        # Find channels ID and names
        channels = self.pixels.findall("{%s}Channel" % self.ns)
        if 'Name' in channels[0].attrib.keys():
            md['Channels'] = list(map(lambda x: x.attrib['Name'], channels))

        # Find dt
        if "TimeIncrement" in self.pixels.attrib.keys():
            dt = float(self.pixels.attrib["TimeIncrement"])
            if dt != 0:
                md['TimeIncrement'] = dt

        if 'TimeIncrement' not in md.keys() or (md['TimeIncrement'] == 0):
            if self.planes and 'DeltaT' in self.planes[0].attrib.keys():
                pl = self.df_planes(['DeltaT'])
                t = pl.xs(0, level='TheC').xs(0, level='TheZ')['DeltaT']
                md['TimeIncrement'] = float(np.diff(t.values).mean())

        # Find distance between slices
        if ('PhysicalSizeZ' not in md.keys()
            and self.planes
            and 'PositionZ' in self.planes[0].attrib.keys()):
            pl = self.df_planes(['PositionZ'])
            z = pl.xs(0, level="TheC")['PositionZ'].groupby(level='TheT')
            z = z.apply(lambda x: np.diff(x.values).mean())
            z = np.abs(z.mean())
            md['PhysicalSizeZ'] = float(z)

        return md

    def tostring(self):
        """Write in memory OME XML to string.

        Returns
        -------
        output: str
            OME XML as string

        """


        et = ElementTree.ElementTree(self.root)
        if sys.version_info[0] < 3:
            f = tempfile.NamedTemporaryFile()
            et.write(f, encoding='utf-8', xml_declaration=True,
                     default_namespace=None)
            f.seek(0)
            output = ''.join(f.readlines())
        else:
            f = io.StringIO()
            et.write(f, encoding='unicode', xml_declaration=True,
                     default_namespace=None)
            output = f.getvalue()
        f.close()

        output = output.replace('<ns0:OME', '<ns0:OME xmlns="%s"' % self.ns)
        return output

    def set_xy_size(self, size_x, size_y):
        """Set X and Y size.

        Parameters
        ----------
        size_x: int
            X size
        size_y: int
            Y size

        """

        self.pixels.attrib['SizeX'] = str(size_x)
        self.pixels.attrib['SizeY'] = str(size_y)

    def set_z_size(self, size_z):
        """Set Z size.

        Parameters
        ----------
        size_z: int
            Z size

        """

        self.pixels.attrib['SizeZ'] = str(size_z)

    def set_physical_size(self, size_x=None, size_y=None, size_z=None):
        """Set physical X, Y and Z size (in um).

        Parameters
        ----------
        size_x: float
            Physicial size for x pixels in um
        size_x: float
            Physicial size for x pixels in um
        size_x: float
            Physicial size for x pixels in um

        """

        if size_x:
            self.pixels.attrib['PhysicalSizeX'] = str(size_x)
        if size_y:
            self.pixels.attrib['PhysicalSizeY'] = str(size_y)
        if size_z:
            self.pixels.attrib['PhysicalSizeZ'] = str(size_z)

    def get_physical_size(self):
        """Get physical size for each dimensions (X, Y and Z) if possible.

        Returns
        -------
        physical_size: dict
            Contains physical size for available dimensions

        """

        res = {}
        if 'PhysicalSizeX' in self.pixels.attrib.keys():
            res['PhysicalSizeX'] = self.pixels.attrib['PhysicalSizeX']
        if 'PhysicalSizeY' in self.pixels.attrib.keys():
            res['PhysicalSizeY'] = self.pixels.attrib['PhysicalSizeY']
        if 'PhysicalSizeZ' in self.pixels.attrib.keys():
            res['PhysicalSizeZ'] = self.pixels.attrib['PhysicalSizeZ']

        return res

    def set_name(self, new_name): # pragma: no cover
        """Set first Image tag name.

        Parameters
        ----------
        new_name: str
            New name to set

        """

        self.img.attrib['Name'] = new_name

    def set_filename(self, new_file_name): # pragma: no cover
        """Set new filename for each TiffData

        Notes
        -----
        Filename will be the same for each TiffData. Do not use if you're dataset
        use several Tiff files.

        Parameters
        -----------
        new_file_name: str
            New filename to set

        """

        uuid_value = uuid.uuid1()
        for p in self.pixels.findall("{%s}TiffData" % self.ns):
            uuid_tag = p.find('{%s}UUID' % self.ns)
            uuid_tag.attrib['FileName'] = new_file_name
            uuid_tag.text = "urn:uuid:" + str(uuid_value)

    def set_size_t(self): # pragma: no cover
        """Set correct size for T dimensions in Plane according to Plane tag.
        """

        size_t = int(self.pixels.findall("{%s}Plane" % self.ns)[-1].attrib['TheT']) + 1

        self.pixels.attrib["SizeT"] = str(size_t)

    def uniform_ifd(self): # pragma: no cover
        """OME with more than one Tiff file has to be converted before save them
        in a single Tiff file to make correct IFD in TiffData tags.

        """

        fnames = []
        last_ifd = None
        last_td = None
        increment_ifd = None

        for td in self.pixels.findall("{%s}TiffData" % self.ns):
            fname = td.find("{%s}UUID" % self.ns).attrib['FileName']
            ifd = int(td.attrib['IFD'])

            if fname not in fnames:
                fnames.append(fname)

            if last_td and ifd == 0:
                last_ifd = int(last_td.attrib['IFD'])
                increment_ifd = last_ifd + 1

            if len(fnames) >= 2 and fname != fnames[-2]:
                ifd += increment_ifd
                td.attrib['IFD'] = str(ifd)

            last_td = td
