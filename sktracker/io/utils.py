import os
import re

import shutil
import logging, warnings

log = logging.getLogger(__name__)

_EXTENSIONS = ('tif', 'tiff', 'TIF',
               'TIFF', 'STK')

def load_img_list(directory):
    '''Loads a list of images from `directory`.

    To be recognized as an image and thus loaded, a file must end with
    either of the extensions defined in the variable `_EXTENSION`.

    Parameter
    ---------
    diretory: str, a path to an existing directory

    Returns
    -------
    img_list: list of strings: the file paths to the images,
        with the file names appended to the included directory
    '''
    img_list = os.listdir(directory)
    img_list.sort(key=_alphanum_key)
    img_list = [os.path.join(directory, imname)
                for imname in img_list if _looks_like_tif(imname)]
    log.info('First file: {}\n'
             'Last file: {}'.format(img_list[0], img_list[-1]))
    return img_list

def _looks_like_tif(fname):
    return any([fname.endswith(ext) for ext in _EXTENSIONS])

def _alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [_tryint(c) for c in re.split('([0-9]+)', s) ]

def _tryint(s):
    try:
        return int(s)
    except ValueError:
        return s
