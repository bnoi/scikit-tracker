import os
import struct
import zipfile
import logging

log = logging.getLogger(__name__)

__all__ = ['read_roi']


def read_roi(roi_path):
    """Read ROI files .zip or .roi generated with ImageJ.
    Specifications and code is largely inspired from:
    http://rsb.info.nih.gov/ij/developer/source/ij/io/RoiDecoder.java.html

    Parameters
    ----------
    roi_path : string
        Path to ROI file (can be either .zip or .roi)

    Returns
    -------
    rois : dict

    Notes
    -----

    - Some format specifications are not implemented. See RoiDecoder.java for details.
    - Most of "normal" ROI file should work.
    - Code has not been yet strongly tested.
    - Feel free to hack it and send me modifications.
    - Star me on gist to show me wether this script has been usefull to you !

    Examples
    --------

    >>> import read_roi
    >>> zip_file = "roi_objects.zip"
    >>> print(read_roi.read_roi_zip(zip_file))
    {'1454-0095-0083': {'y': [7, 19, 27, 40, 56, 74, 96, 120, 134, 152, 183, 182, 171, 151, 140, 117, 92, 65, 51, 50, 35, 21, 11], 'x': [45, 20, 12, 12, 15, 28, 43, 44, 53, 77, 123, 141, 154, 153, 147, 146, 137, 120, 101, 93, 74, 65, 61], 'position': {'channel': 2, 'frame': 73, 'slice': 7}, 'name': '1454-0095-0083', 'n': 23, 'type': 'polygon'}, '0714-0092-0090': {'y': [4, 16, 24, 37, 53, 71, 93, 117, 131, 149, 180, 179, 168, 148, 137, 114, 89, 62, 48, 47, 32, 18, 8], 'x': [52, 27, 19, 19, 22, 35, 50, 51, 60, 84, 130, 148, 161, 160, 154, 153, 144, 127, 108, 100, 81, 72, 68], 'position': {'channel': 2, 'frame': 36, 'slice': 7}, 'name': '0714-0092-0090', 'n': 23, 'type': 'polygon'}, '0014-0089-0092': {'y': [1, 13, 21, 34, 50, 68, 90, 114, 128, 146, 177, 176, 165, 145, 134, 111, 86, 59, 45, 44, 29, 15, 5], 'x': [54, 29, 21, 21, 24, 37, 52, 53, 62, 86, 132, 150, 163, 162, 156, 155, 146, 129, 110, 102, 83, 74, 70], 'position': {'channel': 2, 'frame': 1, 'slice': 7}, 'name': '0014-0089-0092', 'n': 23, 'type': 'polygon'}}

    >>> import read_roi
    >>> roi_file = "roi_object.roi"
    >>> print(read_roi.read_roi(roi_file))
    {'example2': {'y': [7, 19, 27, 40, 56, 74, 96, 120, 134, 152, 183, 182, 171, 151, 140, 117, 92, 65, 51, 50, 35, 21, 11], 'x': [45, 20, 12, 12, 15, 28, 43, 44, 53, 77, 123, 141, 154, 153, 147, 146, 137, 120, 101, 93, 74, 65, 61], 'position': {'channel': 2, 'frame': 73, 'slice': 7}, 'name': 'example2', 'n': 23, 'type': 'polygon'}}

    """

    if roi_path.endswith('.zip'):
        return read_roi_zip(roi_path)
    elif roi_path.endswith('.roi'):
        return read_roi_single(roi_path)
    else:
        log.error("{} doesn't end with .roi or .zip.")


OFFSET = dict(VERSION_OFFSET=4,
              TYPE=6,
              TOP=8,
              LEFT=10,
              BOTTOM=12,
              RIGHT=14,
              N_COORDINATES=16,
              X1=18,
              Y1=22,
              X2=26,
              Y2=30,
              XD=18,
              YD=22,
              WIDTHD=26,
              HEIGHTD=30,
              STROKE_WIDTH=34,
              SHAPE_ROI_SIZE=36,
              STROKE_COLOR=40,
              FILL_COLOR=44,
              SUBTYPE=48,
              OPTIONS=50,
              ARROW_STYLE=52,
              ELLIPSE_ASPECT_RATIO=52,
              ARROW_HEAD_SIZE=53,
              ROUNDED_RECT_ARC_SIZE=54,
              POSITION=56,
              HEADER2_OFFSET=60,
              COORDINATES=64)

ROI_TYPE = dict(polygon=0,
                rect=1,
                oval=2,
                line=3,
                freeline=4,
                polyline=5,
                noRoi=6,
                freehand=7,
                traced=8,
                angle=9,
                point=10)

OPTIONS = dict(SPLINE_FIT=1,
               DOUBLE_HEADED=2,
               OUTLINE=4,
               OVERLAY_LABELS=8,
               OVERLAY_NAMES=16,
               OVERLAY_BACKGROUNDS=32,
               OVERLAY_BOLD=64,
               SUB_PIXEL_RESOLUTION=128,
               DRAW_OFFSET=256)

HEADER_OFFSET = dict(C_POSITION=4,
                     Z_POSITION=8,
                     T_POSITION=12,
                     NAME_OFFSET=16,
                     NAME_LENGTH=20,
                     OVERLAY_LABEL_COLOR=24,
                     OVERLAY_FONT_SIZE=28,
                     AVAILABLE_BYTE1=30,
                     IMAGE_OPACITY=31,
                     IMAGE_SIZE=32,
                     FLOAT_STROKE_WIDTH=36)

SUBTYPES = dict(TEXT=1,
                ARROW=2,
                ELLIPSE=3,
                IMAGE=4)


def get_byte(data, base):
    if isinstance(base, int):
        return data[base]
    elif isinstance(base, list):
        return [data[b] for b in base]


def get_short(data, base):
    b0 = data[base]
    b1 = data[base + 1]
    n = (b0 << 8) + b1
    return n


def get_int(data, base):
    b0 = data[base]
    b1 = data[base + 1]
    b2 = data[base + 2]
    b3 = data[base + 3]
    n = ((b0 << 24) + (b1 << 16) + (b2 << 8) + b3)
    return n


def get_float(data, base):
    return float(get_int(data, base))


def read_roi_single(fpath):
    """
    """

    if isinstance(fpath, zipfile.ZipExtFile):
        data = fpath.read()
        name = os.path.splitext(os.path.basename(fpath.name))[0]
    elif isinstance(fpath, str):
        fp = open(fpath, 'rb')
        data = fp.read()
        fp.close()
        name = os.path.splitext(os.path.basename(fpath))[0]
    else:
        # raise an error
        return None

    size = len(data)
    code = '>'

    roi = {}

    magic = get_byte(data, list(range(4)))
    magic = "".join([chr(c) for c in magic])

    # TODO: raise error if magic != 'Iout'

    version = get_short(data, OFFSET['VERSION_OFFSET'])
    type = get_byte(data, OFFSET['TYPE'])
    subtype = get_short(data, OFFSET['SUBTYPE'])
    top = get_short(data, OFFSET['TOP'])
    left = get_short(data, OFFSET['LEFT'])

    if top > 6000:
        top -= 2**16
    if left > 6000:
        left -= 2**16

    bottom = get_short(data, OFFSET['BOTTOM'])
    right = get_short(data, OFFSET['RIGHT'])
    width = right - left
    height = bottom - top
    n = get_short(data, OFFSET['N_COORDINATES'])
    options = get_short(data, OFFSET['OPTIONS'])
    position = get_int(data, OFFSET['POSITION'])
    hdr2Offset = get_int(data, OFFSET['HEADER2_OFFSET'])

    sub_pixel_resolution = (options == OPTIONS['SUB_PIXEL_RESOLUTION']) and version >= 222
    draw_offset = sub_pixel_resolution and (options == OPTIONS['DRAW_OFFSET'])
    sub_pixel_rect = version >= 223 and sub_pixel_resolution and (roi_type == ROI_TYPE['rect'] or roi_type == ROI_TYPE['oval'])

    # Untested
    if sub_pixel_rect:
        packed_data = fp.read(16)
        s = struct.Struct(code + '4f')
        xd, yd, widthd, heightd = s.unpack(packed_data)

    # Untested
    if hdr2Offset > 0 and hdr2Offset + HEADER_OFFSET['IMAGE_SIZE'] + 4 <= size:
        channel = get_int(data, hdr2Offset + HEADER_OFFSET['C_POSITION'])
        slice = get_int(data, hdr2Offset + HEADER_OFFSET['Z_POSITION'])
        frame = get_int(data, hdr2Offset + HEADER_OFFSET['T_POSITION'])
        overlayLabelColor = get_int(data, hdr2Offset + HEADER_OFFSET['OVERLAY_LABEL_COLOR'])
        overlayFontSize = get_short(data, hdr2Offset + HEADER_OFFSET['OVERLAY_FONT_SIZE'])
        imageOpacity = get_byte(data, hdr2Offset + HEADER_OFFSET['IMAGE_OPACITY'])
        imageSize = get_int(data, hdr2Offset + HEADER_OFFSET['IMAGE_SIZE'])

    is_composite = get_int(data, OFFSET['SHAPE_ROI_SIZE']) > 0

    # Not implemented
    if is_composite:
        if version >= 218:
            # Not implemented
            pass
        if channel > 0 or slice > 0 or frame > 0:
            pass

    if type == ROI_TYPE['rect']:
        roi = {'type': 'rectangle'}

        if sub_pixel_rect:
            roi.update(dict(left=xd, top=yd, width=widthd, height=heightd))
        else:
            roi.update(dict(left=left, top=top, width=width, height=height))

        roi['arc_size'] = get_short(data, OFFSET['ROUNDED_RECT_ARC_SIZE'])

    elif type == ROI_TYPE['oval']:
        roi = {'type': 'oval'}

        if sub_pixel_rect:
            roi.update(dict(left=xd, top=yd, width=widthd, height=heightd))
        else:
            roi.update(dict(left=left, top=top, width=width, height=height))

    elif type == ROI_TYPE['line']:
        roi = {'type': 'line'}

        x1 = get_float(data, OFFSET['X1'])
        y1 = get_float(data, OFFSET['Y1'])
        x2 = get_float(data, OFFSET['X2'])
        y2 = get_float(data, OFFSET['Y2'])

        if subtype == SUBTYPES['ARROW']:
            # Not implemented
            pass
        else:
            roi.update(dict(x1=x1, x2=x2, y1=y1, y2=y2))
            roi['draw_offset'] = draw_offset

    elif type in [ROI_TYPE[t] for t in ["polygon", "freehand", "traced", "polyline", "freeline", "angle", "point"]]:
        x = []
        y = []
        base1 = OFFSET['COORDINATES']
        base2 = base1 + 2 * n
        for i in range(n):
            xtmp = get_short(data, base1 + i * 2)
            if xtmp < 0:
                xtmp = 0
            ytmp = get_short(data, base2 + i * 2)
            if ytmp < 0:
                ytmp = 0
            x.append(left + xtmp)
            y.append(top + ytmp)

        if sub_pixel_resolution:
            xf = []
            yf = []
            base1 = OFFSET['COORDINATES'] + 4 * n
            base2 = base1 + 4 * n
            for i in range(n):
                xf.append(get_float(data, base1 + i * 4))
                yf.append(get_float(data, base2 + i * 4))

        if type == ROI_TYPE['point']:
            roi = {'type': 'point'}

            if sub_pixel_resolution:
                roi.update(dict(x=xf, y=yf, n=n))
            else:
                roi.update(dict(x=x, y=y, n=n))

        if type == ROI_TYPE['polygon']:
            roi = {'type': 'polygon'}
        elif type == ROI_TYPE['freehand']:
            roi = {'type': 'freehand'}
            if subtype == SUBTYPES['ELLIPSE']:
                ex1 = get_float(data, OFFSET['X1'])
                ey1 = get_float(data, OFFSET['Y1'])
                ex2 = get_float(data, OFFSET['X2'])
                ey2 = get_float(data, OFFSET['Y2'])
                roi['aspect_ratio'] = get_float(data, OFFSET['ELLIPSE_ASPECT_RATIO'])
                roi.update(dict(ex1=ex1, ey1=ey1, ex2=ex2, ey2=ey2))

        elif type == ROI_TYPE['traced']:
            roi = {'type': 'traced'}
        elif type == ROI_TYPE['polyline']:
            roi = {'type': 'polyline'}
        elif type == ROI_TYPE['freeline']:
            roi = {'type': 'freeline'}
        elif type == ROI_TYPE['angle']:
            roi = {'type': 'angle'}
        else:
            roi = {'type': 'freeroi'}

        if sub_pixel_resolution:
            roi.update(dict(x=xf, y=yf, n=n))
        else:
            roi.update(dict(x=x, y=y, n=n))
    else:
        # TODO: raise an error for 'Unrecognized ROI type'
        pass

    roi['name'] = name

    if version >= 218:
        # Not implemented
        # Read stroke width, stroke color and fill color
        pass

    if version >= 218 and subtype == SUBTYPES['TEXT']:
        # Not implemented
        # Read test ROI
        pass

    if version >= 218 and subtype == SUBTYPES['IMAGE']:
        # Not implemented
        # Get image ROI
        pass

    roi['position'] = position
    if channel > 0 or slice > 0 or frame > 0:
        roi['position'] = dict(channel=channel, slice=slice, frame=frame)

    return {name: roi}


def read_roi_zip(zip_path):
    """
    """
    rois = {}
    zf = zipfile.ZipFile(zip_path)
    for n in zf.namelist():
        rois.update(read_roi_single(zf.open(n)))
    return rois
