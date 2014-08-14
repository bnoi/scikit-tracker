
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

Trajectories creation
---------------------

All you need to create a ``Trajectories`` object is a
``pandas.DataFrame``. Note that ``sktracker`` makes an heavy use of
``pandas.DataFrame``. If you are not familiar with it, take a look at
the wonderfull `Pandas
documentation <http://pandas.pydata.org/pandas-docs/stable/>`__.

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
          <th rowspan="4" valign="top">0</th>
          <th>0</th>
          <td> 0.943588</td>
          <td> 0.268040</td>
          <td> 0.436611</td>
          <td>  0</td>
        </tr>
        <tr>
          <th>1</th>
          <td> 0.484852</td>
          <td> 0.807258</td>
          <td> 0.222027</td>
          <td>  0</td>
        </tr>
        <tr>
          <th>2</th>
          <td> 0.572740</td>
          <td> 0.155965</td>
          <td> 0.728578</td>
          <td>  0</td>
        </tr>
        <tr>
          <th>3</th>
          <td> 0.215663</td>
          <td> 0.472669</td>
          <td> 0.654975</td>
          <td>  0</td>
        </tr>
        <tr>
          <th>1</th>
          <th>4</th>
          <td> 0.449510</td>
          <td> 0.313357</td>
          <td> 0.153198</td>
          <td> 60</td>
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

    2014-08-14 11:17:34:INFO:sktracker.utils.mpl_loader: Matplotlib backend 'Qt4Agg' has been loaded.


                :ref:`create_trajs`
                
Trajectories viewer
-------------------

First thing you want to do is probably to visualize trajectories you're
working on. First load some sample dataset.

.. code:: python

    from sktracker import data
    from sktracker.trajectories import Trajectories
    trajs = data.with_gaps_df()
    trajs = Trajectories(trajs)
    trajs.head()

.. parsed-literal::

    2014-08-14 11:27:02:INFO:sktracker.utils.mpl_loader: Matplotlib backend 'Qt4Agg' has been loaded.




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

    <matplotlib.axes.AxesSubplot at 0x7effe6ca1cc0>




.. image:: trajectories_notebook_output_files/output_10_1.png


You can change axis to display.

.. code:: python

    trajs.show(xaxis='t', yaxis='y')



.. parsed-literal::

    <matplotlib.axes.AxesSubplot at 0x7effde9c5860>




.. image:: trajectories_notebook_output_files/output_12_1.png


You can also add a legend.

.. code:: python

    trajs.show(legend=True)



.. parsed-literal::

    <matplotlib.axes.AxesSubplot at 0x7effde8ef0f0>




.. image:: trajectories_notebook_output_files/output_14_1.png


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

    <matplotlib.axes.AxesSubplot at 0x7effde7d7f28>




.. image:: trajectories_notebook_output_files/output_16_1.png


``Trajectories.show()`` is a nice way to quickly build visualizations.
However ``sktracker.ui`` module provides more complex functions and
classes in order to visualize your trajectories/dataset. See
`here <ui.html>`__ for more details.

                <a id='get_infos' />
                
Retrieve informations
---------------------

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

Automatic objects detection and tracking is very powerfull. However
sometime you'll need to manually edit and modify trajectories. Here it
is presented methods to help you with that. Methods are separated in two
kinds : global and local trajectories modifications.

Global modifications
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    trajs['t']



.. parsed-literal::

    t_stamp  label
    0        0         0
             1         0
             2         0
    1        0         1
             1         1
             2         1
    2        0         2
             1         2
             2         2
    3        0         3
             1         3
             2         3
    4        1         4
             2         4
    5        1         5
             2         5
             3         5
    6        2         6
             3         6
    7        2         7
             3         7
             4         7
    8        2         8
             3         8
             4         8
    9        2         9
             3         9
             4         9
    10       2        10
             3        10
             4        10
    11       2        11
             3        11
             4        11
    12       2        12
             3        12
             4        12
    13       2        13
             3        13
             4        13
    14       3        14
             4        14
    15       3        15
             4        15
             5        15
    16       3        16
             4        16
             5        16
    17       4        17
             5        17
    18       4        18
             5        18
             6        18
    19       4        19
             5        19
             6        19
    Name: t, Length: 56, dtype: float64



Measurements on trajectories
----------------------------

TODO

.. code:: python

    # Run this cell first.
    %load_ext autoreload
    %autoreload 2