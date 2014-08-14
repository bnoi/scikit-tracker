
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
          <th rowspan="3" valign="top">0</th>
          <th>0</th>
          <td> 0.266288</td>
          <td> 0.741809</td>
          <td> 0.727173</td>
          <td>  0</td>
        </tr>
        <tr>
          <th>1</th>
          <td> 0.151043</td>
          <td> 0.094702</td>
          <td> 0.045460</td>
          <td>  0</td>
        </tr>
        <tr>
          <th>2</th>
          <td> 0.621466</td>
          <td> 0.857687</td>
          <td> 0.303807</td>
          <td>  0</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">1</th>
          <th>3</th>
          <td> 0.019421</td>
          <td> 0.216775</td>
          <td> 0.218089</td>
          <td> 60</td>
        </tr>
        <tr>
          <th>4</th>
          <td> 0.325111</td>
          <td> 0.014488</td>
          <td> 0.505610</td>
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

    2014-08-14 14:01:32:INFO:sktracker.utils.mpl_loader: Matplotlib backend 'Qt4Agg' has been loaded.


Trajectories viewer
-------------------

First thing you want to do is probably to visualize trajectories you're
working on. First load some sample dataset.

.. code:: python

    import numpy as np
    from sktracker import data
    from sktracker.trajectories import Trajectories
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

    <matplotlib.axes.AxesSubplot at 0x2b060cc05fd0>




.. image:: trajectories_notebook_output_files/output_9_1.png


You can change axis to display.

.. code:: python

    trajs.show(xaxis='t', yaxis='y')



.. parsed-literal::

    <matplotlib.axes.AxesSubplot at 0x2b060ec54978>




.. image:: trajectories_notebook_output_files/output_11_1.png


You can also add a legend.

.. code:: python

    trajs.show(legend=True)



.. parsed-literal::

    <matplotlib.axes.AxesSubplot at 0x2b060ecfd4e0>




.. image:: trajectories_notebook_output_files/output_13_1.png


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

    <matplotlib.axes.AxesSubplot at 0x2b060ee680f0>




.. image:: trajectories_notebook_output_files/output_15_1.png


``Trajectories.show()`` is a nice way to quickly build visualizations.
However ``sktracker.ui`` module provides more complex functions and
classes in order to visualize your trajectories/dataset. See
`here <ui.html>`__ for more details.

Retrieve informations
---------------------

Here you will find how to retrieve informations specific to
trajectories. Remember that trajectory and segment are the same as well
as object/peak and spot are the same.

.. code:: python

    import numpy as np
    from sktracker import data
    from sktracker.trajectories import Trajectories
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
kinds : *global* and *local* trajectories modifications.

.. code:: python

    import numpy as np
    from sktracker import data
    from sktracker.trajectories import Trajectories
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



Global modifications
~~~~~~~~~~~~~~~~~~~~

Reverse trajectories according to a column (time column makes sense most
of the time :-))

.. code:: python

    reversed_traj = trajs.reverse(time_column='t', inplace=False)
    print(reversed_traj['t'].head())

.. parsed-literal::

    t_stamp  label
    -19      6       -19
             5       -19
             4       -19
    -18      6       -18
             5       -18
    Name: t, dtype: float64


Merge two trajectories together taking care to not mix labels.

.. code:: python

    print("Original trajs labels:", trajs.labels)
    merged_trajs = trajs.merge(trajs.copy())
    print("Merged trajs new labels:", merged_trajs.labels)

.. parsed-literal::

    Original trajs labels: [0 1 2 3 4 5 6]
    Merged trajs new labels: [ 0  1  2  7  8  9  3 10  4 11  5 12  6 13]


Relabel trajectories from zero. Note that it will also sort labels
order.

.. code:: python

    print("Original trajs labels:", merged_trajs.labels)
    relabeled_trajs = merged_trajs.relabel_fromzero()
    print("Relabeled trajs labels:", relabeled_trajs.labels)

.. parsed-literal::

    Original trajs labels: [ 0  1  2  7  8  9  3 10  4 11  5 12  6 13]
    Relabeled trajs labels: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13]


``time_interpolate()`` can "fill" holes in your dataset. For example if
you have trajs with a missing timepoint, this method will try to "guess"
the value of the missing timepoint.

.. code:: python

    # t = 1 is missing here
    missing_trajs = Trajectories(trajs[trajs['t'] != 1])
    missing_trajs.head(10)



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
          <th rowspan="3" valign="top">2</th>
          <th>0</th>
          <td>-13.063704</td>
          <td>  2.757048</td>
          <td> -8.495509</td>
          <td> 0</td>
          <td> 2</td>
        </tr>
        <tr>
          <th>1</th>
          <td> -1.044417</td>
          <td> 13.936055</td>
          <td>  9.996726</td>
          <td> 1</td>
          <td> 2</td>
        </tr>
        <tr>
          <th>2</th>
          <td>-19.295839</td>
          <td>  9.188858</td>
          <td>  3.061227</td>
          <td> 2</td>
          <td> 2</td>
        </tr>
        <tr>
          <th rowspan="3" valign="top">3</th>
          <th>0</th>
          <td>-13.679896</td>
          <td>  3.493356</td>
          <td> -9.183014</td>
          <td> 0</td>
          <td> 3</td>
        </tr>
        <tr>
          <th>1</th>
          <td> -0.571843</td>
          <td> 15.075394</td>
          <td> 10.780867</td>
          <td> 1</td>
          <td> 3</td>
        </tr>
        <tr>
          <th>2</th>
          <td>-19.159403</td>
          <td>  9.857153</td>
          <td>  2.096635</td>
          <td> 2</td>
          <td> 3</td>
        </tr>
        <tr>
          <th>4</th>
          <th>1</th>
          <td>  0.545050</td>
          <td> 14.743210</td>
          <td> 12.023129</td>
          <td> 1</td>
          <td> 4</td>
        </tr>
      </tbody>
    </table>
    </div>



The method return a new ``Trajectories`` with interpolated value for
missing timepoint. ``v_*`` values are speeds and ``a_*`` values are
accelerations.

.. code:: python

    # t = 1 has been "guessed"
    interpolated_trajs = missing_trajs.time_interpolate()
    interpolated_trajs.head(10)



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>t</th>
          <th>x</th>
          <th>v_x</th>
          <th>a_x</th>
          <th>y</th>
          <th>v_y</th>
          <th>a_y</th>
          <th>z</th>
          <th>v_z</th>
          <th>a_z</th>
        </tr>
        <tr>
          <th>t_stamp</th>
          <th>label</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
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
          <td> 0</td>
          <td>-15.425890</td>
          <td> 1.181093</td>
          <td>      NaN</td>
          <td>  3.604392</td>
          <td>-0.423672</td>
          <td>      NaN</td>
          <td> -9.723257</td>
          <td> 0.613874</td>
          <td>      NaN</td>
        </tr>
        <tr>
          <th>1</th>
          <td> 0</td>
          <td> -0.419929</td>
          <td>-0.475633</td>
          <td>-0.076494</td>
          <td> 17.429072</td>
          <td>-7.163935</td>
          <td> 7.746446</td>
          <td> 10.077393</td>
          <td>-0.273943</td>
          <td> 0.022917</td>
        </tr>
        <tr>
          <th>2</th>
          <td> 0</td>
          <td>-18.238856</td>
          <td>-1.830310</td>
          <td> 1.874175</td>
          <td>  7.356460</td>
          <td>-0.272637</td>
          <td> 2.091574</td>
          <td>  1.138426</td>
          <td> 3.899341</td>
          <td>-4.040572</td>
        </tr>
        <tr>
          <th rowspan="3" valign="top">1</th>
          <th>0</th>
          <td> 1</td>
          <td>-14.244797</td>
          <td> 1.181093</td>
          <td>      NaN</td>
          <td>  3.180720</td>
          <td>-0.423672</td>
          <td>      NaN</td>
          <td> -9.109383</td>
          <td> 0.613874</td>
          <td>      NaN</td>
        </tr>
        <tr>
          <th>1</th>
          <td> 1</td>
          <td> -0.873838</td>
          <td>-0.372215</td>
          <td> 0.283330</td>
          <td> 13.556105</td>
          <td>-1.164254</td>
          <td> 4.252917</td>
          <td>  9.867582</td>
          <td>-0.093007</td>
          <td> 0.338956</td>
        </tr>
        <tr>
          <th>2</th>
          <td> 1</td>
          <td>-19.275168</td>
          <td>-0.385402</td>
          <td> 1.015641</td>
          <td>  7.903925</td>
          <td> 1.141883</td>
          <td> 0.737468</td>
          <td>  3.293139</td>
          <td> 0.685742</td>
          <td>-2.386626</td>
        </tr>
        <tr>
          <th rowspan="3" valign="top">2</th>
          <th>0</th>
          <td> 2</td>
          <td>-13.063704</td>
          <td>-0.616192</td>
          <td>      NaN</td>
          <td>  2.757048</td>
          <td> 0.736307</td>
          <td>      NaN</td>
          <td> -8.495509</td>
          <td>-0.687505</td>
          <td>      NaN</td>
        </tr>
        <tr>
          <th>1</th>
          <td> 2</td>
          <td> -1.044417</td>
          <td> 0.091027</td>
          <td> 0.643154</td>
          <td> 13.936055</td>
          <td> 1.341899</td>
          <td> 0.759388</td>
          <td>  9.996726</td>
          <td> 0.403969</td>
          <td> 0.654996</td>
        </tr>
        <tr>
          <th>2</th>
          <td> 2</td>
          <td>-19.295839</td>
          <td> 0.200972</td>
          <td> 0.157107</td>
          <td>  9.188858</td>
          <td> 1.202298</td>
          <td>-0.616639</td>
          <td>  3.061227</td>
          <td>-0.873910</td>
          <td>-0.732679</td>
        </tr>
        <tr>
          <th>3</th>
          <th>0</th>
          <td> 3</td>
          <td>-13.679896</td>
          <td>-0.616192</td>
          <td>      NaN</td>
          <td>  3.493356</td>
          <td> 0.736307</td>
          <td>      NaN</td>
          <td> -9.183014</td>
          <td>-0.687505</td>
          <td>      NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



See also:

-  ``relabel()``
-  ``scale()``
-  ``project()`` : project each spots on a line specified by two spots.

See ```Trajectories``
API <http://scikit-tracker.org/dev/api/sktracker.trajectories.html#sktracker.trajectories.Trajectories>`__
for more informations.

Local modifications
~~~~~~~~~~~~~~~~~~~

Let's see how to edit trajectories details. Almost in all methods, spots
are identified with a tuple ``(t_stamp, label)`` and trajectory by an
integer ``label``.

Remove a spot (can be a list of spots)

.. code:: python

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

    trajs.remove_spots((0, 2), inplace=False).head()



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
          <th rowspan="2" valign="top">0</th>
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
          <th rowspan="3" valign="top">1</th>
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
        <tr>
          <th>2</th>
          <td>-18.621760</td>
          <td>  9.218586</td>
          <td>  2.633193</td>
          <td> 2</td>
          <td> 1</td>
        </tr>
      </tbody>
    </table>
    </div>



Remove a segment/trajectory

.. code:: python

    trajs.labels



.. parsed-literal::

    array([0, 1, 2, 3, 4, 5, 6])



.. code:: python

    trajs.remove_segments(3).labels



.. parsed-literal::

    array([0, 1, 2, 4, 5, 6])



Merge two segments

.. code:: python

    print("Size of segment #0 :", len(trajs.get_segments()[0]))
    print("Size of segment #3 :", len(trajs.get_segments()[3]))
    
    merged_trajs = trajs.merge_segments((0, 3), inplace=False)
    
    print("Size of segment #0 (merged with #3):", len(merged_trajs.get_segments()[0]))

.. parsed-literal::

    Size of segment #0 : 4
    Size of segment #3 : 12
    Size of segment #0 (merged with #3): 16


Cut a segment

.. code:: python

    print("Size of segment #4:", len(trajs.get_segments()[4]))
    
    cut_trajs = trajs.cut_segments((13, 4), inplace=False)
    
    print("Size of segment #4 :", len(cut_trajs.get_segments()[4]))
    print("Size of segment #7 (new segment after cut) :", len(cut_trajs.get_segments()[7]))

.. parsed-literal::

    Size of segment #4: 13
    Size of segment #4 : 7
    Size of segment #7 (new segment after cut) : 6


Duplicate a segment

.. code:: python

    dupli_trajs = trajs.duplicate_segments(4)
    
    # Check wether #4 and #7 (duplicated) are the same
    np.all(dupli_trajs.get_segments()[4].values == dupli_trajs.get_segments()[7].values)



.. parsed-literal::

    True



Measurements on trajectories
----------------------------

.. code:: python

    from sktracker import data
    from sktracker.trajectories import Trajectories
    trajs = Trajectories(data.brownian_trajs_df())
Get the differences between each consecutive timepoints for a same
trajectory (label).

.. code:: python

    trajs.get_diff().head(15)



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>t</th>
          <th>x</th>
          <th>y</th>
          <th>z</th>
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
          <td>NaN</td>
          <td>       NaN</td>
          <td>       NaN</td>
          <td>       NaN</td>
        </tr>
        <tr>
          <th>1</th>
          <td>NaN</td>
          <td>       NaN</td>
          <td>       NaN</td>
          <td>       NaN</td>
        </tr>
        <tr>
          <th>2</th>
          <td>NaN</td>
          <td>       NaN</td>
          <td>       NaN</td>
          <td>       NaN</td>
        </tr>
        <tr>
          <th>3</th>
          <td>NaN</td>
          <td>       NaN</td>
          <td>       NaN</td>
          <td>       NaN</td>
        </tr>
        <tr>
          <th>4</th>
          <td>NaN</td>
          <td>       NaN</td>
          <td>       NaN</td>
          <td>       NaN</td>
        </tr>
        <tr>
          <th rowspan="5" valign="top">1</th>
          <th>0</th>
          <td>  1</td>
          <td> 20.307078</td>
          <td> -8.108166</td>
          <td>-19.490299</td>
        </tr>
        <tr>
          <th>1</th>
          <td>  1</td>
          <td> 13.827910</td>
          <td> 29.331007</td>
          <td>-23.354528</td>
        </tr>
        <tr>
          <th>2</th>
          <td>  1</td>
          <td>  3.845230</td>
          <td> 14.221569</td>
          <td> 25.614719</td>
        </tr>
        <tr>
          <th>3</th>
          <td>  1</td>
          <td>-30.136494</td>
          <td>-17.332147</td>
          <td>  8.584708</td>
        </tr>
        <tr>
          <th>4</th>
          <td>  1</td>
          <td> -5.692935</td>
          <td>-17.923296</td>
          <td>  7.438539</td>
        </tr>
        <tr>
          <th rowspan="5" valign="top">2</th>
          <th>0</th>
          <td>  1</td>
          <td>  5.629275</td>
          <td> 11.364669</td>
          <td>-14.749773</td>
        </tr>
        <tr>
          <th>1</th>
          <td>  1</td>
          <td>-23.926437</td>
          <td> -2.618648</td>
          <td> 35.080733</td>
        </tr>
        <tr>
          <th>2</th>
          <td>  1</td>
          <td> -3.746919</td>
          <td>-15.052938</td>
          <td>-26.025025</td>
        </tr>
        <tr>
          <th>3</th>
          <td>  1</td>
          <td> 23.240229</td>
          <td>  5.534567</td>
          <td>  4.645337</td>
        </tr>
        <tr>
          <th>4</th>
          <td>  1</td>
          <td>  0.634655</td>
          <td> -0.002195</td>
          <td>  0.283652</td>
        </tr>
      </tbody>
    </table>
    </div>



Get the instantaneous speeds between each consecutive timepoints for a
same trajectory (label).

.. code:: python

    trajs.get_speeds().head(15)



.. parsed-literal::

    t_stamp  label
    0        0                NaN
             1                NaN
             2                NaN
             3                NaN
             4                NaN
    1        0         857.991535
             1        1596.953075
             2         873.152678
             3        1282.308817
             4         408.985890
    2        0         378.400237
             1        1809.989515
             2         917.932277
             3         592.318817
             4           0.483250
    dtype: float64



.. code:: python

    # Run this cell first.
    %load_ext autoreload
    %autoreload 2