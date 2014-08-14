
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

    %matplotlib inline
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
          <th>0</th>
          <th>0</th>
          <td> 0.891366</td>
          <td> 0.659543</td>
          <td> 0.091617</td>
          <td>   0</td>
        </tr>
        <tr>
          <th>1</th>
          <th>1</th>
          <td> 0.602459</td>
          <td> 0.673590</td>
          <td> 0.111075</td>
          <td>  60</td>
        </tr>
        <tr>
          <th rowspan="3" valign="top">2</th>
          <th>2</th>
          <td> 0.907255</td>
          <td> 0.522362</td>
          <td> 0.644981</td>
          <td> 120</td>
        </tr>
        <tr>
          <th>3</th>
          <td> 0.823668</td>
          <td> 0.811170</td>
          <td> 0.229627</td>
          <td> 120</td>
        </tr>
        <tr>
          <th>4</th>
          <td> 0.316576</td>
          <td> 0.700603</td>
          <td> 0.369789</td>
          <td> 120</td>
        </tr>
      </tbody>
    </table>
    </div>



To create ``Trajectories``, dataframe need to have:

-  columns ('x', 'y', 'z', 't' here)
-  a multi index (see `pandas
   doc <http://pandas.pydata.org/pandas-docs/stable/indexing.html#hierarchical-indexing-multiindex>`__)
   with two levels : ``t_stamp`` and ``label``

While ``t_stamp`` and ``label`` are required. Columns can contain
anything you want/need.

.. code:: python

    from sktracker.trajectories import Trajectories
    
    # Create a Trajectories instance
    trajs = Trajectories(trajs)

.. parsed-literal::

    2014-08-14 11:22:55:INFO:sktracker.utils.mpl_loader: Matplotlib backend 'Qt4Agg' has been loaded.



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

    <matplotlib.axes.AxesSubplot at 0x2b9fda13c630>



.. parsed-literal::

    /home/hadim/local/virtualenvs/st/lib/python3.4/site-packages/matplotlib/font_manager.py:1236: UserWarning: findfont: Font family ['monospace'] not found. Falling back to Bitstream Vera Sans
      (prop.get_family(), self.defaultFamily[fontext]))



.. image:: trajectories_notebook_output_files/output_11_2.png


You can change axis to display.

.. code:: python

    trajs.show(xaxis='t', yaxis='y')



.. parsed-literal::

    <matplotlib.axes.AxesSubplot at 0x2b9fdc18f278>




.. image:: trajectories_notebook_output_files/output_13_1.png


You can also add a legend.

.. code:: python

    trajs.show(legend=True)



.. parsed-literal::

    <matplotlib.axes.AxesSubplot at 0x2b9fdc2585f8>




.. image:: trajectories_notebook_output_files/output_15_1.png


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

    <matplotlib.axes.AxesSubplot at 0x2b9fdc3c3f60>




.. image:: trajectories_notebook_output_files/output_17_1.png


``Trajectories.show()`` is a nice way to quickly build visualizations.
However ``sktracker.ui`` module provides more complex functions and
classes in order to visualize your trajectories/dataset. See
`here <ui.html>`__ for more details.

Get informations
----------------

Here you will find how to retrieve informations specific to
trajectories. Remember that trajectory and segment are the same as well
as object/peak and spot are the same.

.. code:: python

    trajs.t_stamps



.. parsed-literal::

    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
           17, 18, 19])



.. code:: python

    # Each label corresponds to one segment/trajectory
    trajs.labels



.. parsed-literal::

    array([0, 1, 2, 3, 4, 5, 6])



.. code:: python

    # Get dict if dataframe index of segments (sorted by labels)
    trajs.segment_idxs[0]



.. parsed-literal::

    [(0, 0), (1, 0), (2, 0), (3, 0)]



.. code:: python

    # Iterator over segments
    for label, segment in trajs.iter_segments:
        print(label, end=' ')

.. parsed-literal::

    0 1 2 3 4 5 6 

.. code:: python

    # Get bounds (first and last spots/objects) of each segment
    trajs.get_bounds()



.. parsed-literal::

    {0: (0, 3),
     1: (0, 5),
     2: (0, 13),
     3: (5, 16),
     4: (7, 19),
     5: (15, 19),
     6: (18, 19)}



.. code:: python

    # Get a different colors for each segments
    trajs.get_colors()



.. parsed-literal::

    {0: '#FF0000',
     1: '#FFE000',
     2: '#3DFF00',
     3: '#00FFA9',
     4: '#0074FF',
     5: '#7200FF',
     6: '#FF00AC'}



Some other methods such as:

-  ``get_segments()``
-  ``get_longest_segments()``
-  ``get_shortest_segments()``
-  ``get_t_stamps_correspondences()``

See ```Trajectories``
API <http://scikit-tracker.org/dev/api/sktracker.trajectories.html#sktracker.trajectories.Trajectories>`__
for more informations.

Modify trajectories
-------------------

TODO

Measurements on trajectories
----------------------------

TODO

.. code:: python

    # Run this cell first.
    %load_ext autoreload
    %autoreload 2