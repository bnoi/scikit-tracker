
Representation of trajectories
==============================

``sktracker.trajectories.Trajectories`` is probably the most important
class in ``sktracker`` as it represents detected objects and links
between them. ``Trajectories`` is a subclass of ``pandas.DataFrame``
which provides convenient methods.

A ``Trajectories`` object consists of several single trajectory. Each
row contains an **object** which has several features (columns) and two
integer as index. The first integer is a time stamp ``t_stamp`` and the
second one is a ``label``. Objects from the same ``label`` belong to the
same trajectory.

Be aware that ``t_stamp`` are time index and does not represent time in
second or minute. Time position (in second or minute) can be stored as
object's features in columns (with 't' for example).

Create trajectories
-------------------

All you need to create a ``Trajectories`` object is a
``pandas.DataFrame``.

.. code:: python

    import pandas as pd
    import numpy as np
    
    trajs = pd.DataFrame(np.random.random((30, 3)), columns=['x', 'y', 'z'])
    trajs['t_stamp'] = np.sort(np.random.choice(range(10), (len(trajs),)))
    trajs['label'] = list(range(len(trajs)))
    trajs['t'] = trajs['t_stamp'] * 60  # t are in seconds for example
    trajs.set_index(['t_stamp', 'label'], inplace=True)
    trajs.sort_index(inplace=True)
    trajs.head()



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>x</th>
          <th>y</th>
          <th>z</th>
          <th>t</th>
        </tr>
        <tr>
          <th>t_stamp</th>
          <th>label</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">0</th>
          <th>0</th>
          <td> 0.004332</td>
          <td> 0.059065</td>
          <td> 0.676030</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>1</th>
          <td> 0.321825</td>
          <td> 0.041608</td>
          <td> 0.573881</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>2</th>
          <td> 0.965764</td>
          <td> 0.254034</td>
          <td> 0.914095</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>3</th>
          <td> 0.032845</td>
          <td> 0.795814</td>
          <td> 0.941050</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>4</th>
          <td> 0.320644</td>
          <td> 0.821060</td>
          <td> 0.030100</td>
          <td> 0</td>
        </tr>
      </tbody>
    </table>
    </div>



To create ``Trajectories``, dataframe need to have: - columns ('x', 'y',
'z', 't' here) - a multi index (see `pandas
doc <http://pandas.pydata.org/pandas-docs/stable/indexing.html#hierarchical-indexing-multiindex>`__)
with two levels : ``t_stamp`` and ``label``

While ``t_stamp`` and ``label`` are required. Columns can contain
anything you want/need.

.. code:: python

    from sktracker.trajectories import Trajectories
    
    # Create a Trajectories instance
    trajs = Trajectories(trajs)
Visualize trajectories
----------------------

First thing you want to do is probably to visualize trajectories you're
working on. First load some sample dataset.

.. code:: python

    from sktracker import data
    
    trajs = data.with_gaps_df()
    trajs = Trajectories(trajs)
    trajs.head()



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>x</th>
          <th>y</th>
          <th>z</th>
          <th>true_label</th>
          <th>t</th>
        </tr>
        <tr>
          <th>t_stamp</th>
          <th>label</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="3" valign="top">0</th>
          <th>0</th>
          <td>-15.425890</td>
          <td>  3.604392</td>
          <td> -9.723257</td>
          <td> 0</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>1</th>
          <td> -0.419929</td>
          <td> 17.429072</td>
          <td> 10.077393</td>
          <td> 1</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>-18.238856</td>
          <td>  7.356460</td>
          <td>  1.138426</td>
          <td> 2</td>
          <td> 0</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">1</th>
          <th>0</th>
          <td>-13.126613</td>
          <td>  2.122316</td>
          <td> -9.375269</td>
          <td> 0</td>
          <td> 1</td>
        </tr>
        <tr>
          <th>1</th>
          <td> -1.217757</td>
          <td> 15.554279</td>
          <td> 10.444372</td>
          <td> 1</td>
          <td> 1</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    trajs.show()



.. parsed-literal::

    <matplotlib.axes.AxesSubplot at 0x7f38a0c09e10>



.. parsed-literal::

    /home/hadim/.virtualenvs/st/lib/python3.4/site-packages/matplotlib/font_manager.py:1236: UserWarning: findfont: Font family ['monospace'] not found. Falling back to Bitstream Vera Sans
      (prop.get_family(), self.defaultFamily[fontext]))



.. image:: basics/trajectories_output_files/output_9_2.png


You can change axis to display.

.. code:: python

    trajs.show(xaxis='t', yaxis='y')



.. parsed-literal::

    <matplotlib.axes.AxesSubplot at 0x7f389d321780>




.. image:: basics/trajectories_output_files/output_11_1.png


You can also add a legend.

.. code:: python

    trajs.show(legend=True)



.. parsed-literal::

    <matplotlib.axes.AxesSubplot at 0x7f389d24d7f0>




.. image:: basics/trajectories_output_files/output_13_1.png


You can also build more complex figures.

.. code:: python

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(15, 3))
    
    ax1 = plt.subplot2grid((1, 3), (0, 0))
    ax2 = plt.subplot2grid((1, 3), (0, 1))
    ax3 = plt.subplot2grid((1, 3), (0, 2))
    
    trajs.show(xaxis='t', yaxis='x', ax=ax1)
    trajs.show(xaxis='t', yaxis='y', ax=ax2)
    trajs.show(xaxis='t', yaxis='z', ax=ax3)



.. parsed-literal::

    <matplotlib.axes.AxesSubplot at 0x7f389ca12a58>




.. image:: basics/trajectories_output_files/output_15_1.png


``Trajectories.show()`` is a nice way to quickly build visualizations.
However ``sktracker.ui`` module provides more complex functions and
classes in order to visualize your trajectories/dataset. See
`here <ui.html>`__ for more details.

Get informations
----------------

Modify trajectories
-------------------

Measurements on trajectories
----------------------------

.. code:: python

    # Run this cell first.
    %matplotlib inline
    %load_ext autoreload
    %autoreload 2
.. code:: python

    import glob
    import fnmatch
.. code:: python

    #working_dir = os.path.dirname(os.path.realpath(__file__))
    working_dir = "/home/hadim/Insync/Documents/phd/dev/scikit-tracker/doc/source"
.. code:: python

    for root, dirs, files in os.walk(working_dir):
        for f in fnmatch.filter(files, '*.ipynb'):
            if ".ipynb_checkpoints" not in root:
                full_path = os.path.join(root, f)
                real_path = os.path.relpath(full_path, working_dir)
                print(full_path)

.. parsed-literal::

    /home/hadim/Insync/Documents/phd/dev/scikit-tracker/doc/source/basics/data.ipynb
    /home/hadim/Insync/Documents/phd/dev/scikit-tracker/doc/source/basics/tracker.ipynb
    /home/hadim/Insync/Documents/phd/dev/scikit-tracker/doc/source/basics/ui.ipynb
    /home/hadim/Insync/Documents/phd/dev/scikit-tracker/doc/source/basics/trajectories.ipynb
    /home/hadim/Insync/Documents/phd/dev/scikit-tracker/doc/source/basics/io.ipynb
    /home/hadim/Insync/Documents/phd/dev/scikit-tracker/doc/source/basics/detection.ipynb


.. code:: python

    output_dirs = "/home/hadim/Insync/Documents/phd/dev/scikit-tracker/doc/source/_static/"
    full_path = "/home/hadim/Insync/Documents/phd/dev/scikit-tracker/doc/source/basics/trajectories.ipynb"
    rel_path = "basics/trajectories.ipynb"
.. code:: python

    import os
    
    from IPython.nbformat import current as nbformat
    from IPython.nbconvert import RSTExporter
    from IPython.nbconvert.writers import FilesWriter
    
    nb = nbformat.reads_json(open(full_path).read())
    exporter = RSTExporter()
    writer =  FilesWriter()
.. code:: python

    resources = {}
    nb_name = os.path.splitext(os.path.basename(full_path))[0]
    nb_output_dirs = os.path.join(os.path.dirname(rel_path), nb_name + "_output_files")
    resources['output_files_dir'] = nb_output_dirs
    
    (output, resources) = exporter.from_filename(full_path, resources=resources)
    nb_name = resources['metadata']['name']
    
    #resources['output_files_dir'] = '/home/hadim/test'
    
    writer.build_directory = os.path.dirname(full_path)
    writer.write(output, resources, notebook_name=nb_name)



.. parsed-literal::

    '/home/hadim/Insync/Documents/phd/dev/scikit-tracker/doc/source/basics/trajectories.rst'



.. code:: python

    resources['output_files_dir']



.. parsed-literal::

    ''


