"""
This script is very ugly and I hope someone will improve it but it does the job and it's all I ask
for now.

Put the script in the parent directory of your source/ sphinx dir. In the source/ folder you should
have the _static/ dir.

The script will look for all .ipynb files in source/ and convert them at the same place in .rst
files.

Building html doc with sphinx should then display your notebooks perfectly and with figures.

Please hack this script and share it ! Or better build a sphinx extension and I will buy you a beer
(I am sure I won't be alone) !

Date : 11/08/2014
Author : HadiM <hadrien.mary@gmail.com>
License : WTFPL
"""

import fnmatch
import os

from IPython.nbformat import current as nbformat
from IPython.nbconvert import RSTExporter
from IPython.nbconvert.writers import FilesWriter

if __name__ == '__main__':

    source_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "source")
    static_dirs = os.path.join(source_dir, "_static/")

    for root, dirs, files in os.walk(source_dir):
        if ".ipynb_checkpoints" in root:
            continue

        nb_files = fnmatch.filter(files, '*.ipynb')
        for f in nb_files:

            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, source_dir)
            print(rel_path)

            build_dir = os.path.dirname(full_path)
            rel_build_dir = os.path.relpath(build_dir, source_dir)

            nb = nbformat.reads_json(open(full_path).read())
            exporter = RSTExporter()
            writer = FilesWriter()

            resources = {}
            nb_name = os.path.splitext(os.path.basename(full_path))[0]
            nb_output_dirs = nb_name + "_notebook_output_files"
            resources['output_files_dir'] = nb_output_dirs

            (output, resources) = exporter.from_filename(full_path, resources=resources)
            nb_name = resources['metadata']['name']

            writer.build_directory = build_dir
            writer.write(output, resources, notebook_name=nb_name)
