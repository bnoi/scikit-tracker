
Ready to use test dataset
=========================

``sktracker`` provides a ``data`` module contains sample dataset in
order to test or usefulle during development.

.. code:: python

    %matplotlib inline
    import matplotlib.pyplot as plt
    
    import pandas as pd
    
    from sktracker import data
    from sktracker.trajectories import Trajectories
    from sktracker.io import TiffFile

.. parsed-literal::

    2014-08-14 14:37:03:INFO:sktracker.utils.mpl_loader: Matplotlib backend 'Qt4Agg' has been loaded.


Generate brownian or directed trajectories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    trajs = Trajectories(data.brownian_trajectories_generator())
    trajs.show(groupby_args={'by': 'true_label'})



.. parsed-literal::

    <matplotlib.axes.AxesSubplot at 0x2b88b68adfd0>




.. image:: data_notebook_output_files/output_3_1.png


.. code:: python

    trajs = Trajectories(data.directed_trajectories_generator())
    trajs.show(groupby_args={'by': 'true_label'})



.. parsed-literal::

    <matplotlib.axes.AxesSubplot at 0x2b88b69925c0>




.. image:: data_notebook_output_files/output_4_1.png


Get sample microscopy stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    tf = TiffFile(data.CZT_peaks())
    arr = tf.asarray()
    print("Shape is :", arr.shape)
    
    a = arr[0, 0, 0]
    plt.imshow(a, interpolation='none', cmap='gray')

.. parsed-literal::

    Shape is : (1, 4, 4, 48, 56)




.. parsed-literal::

    <matplotlib.image.AxesImage at 0x2b88b6a711d0>




.. image:: data_notebook_output_files/output_6_2.png


Get Tiff files as filenames list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    data.stack_list()



.. parsed-literal::

    ['/home/hadim/Insync/Documents/phd/dev/scikit-tracker/sktracker/data/stack_list/Stack-1.tif',
     '/home/hadim/Insync/Documents/phd/dev/scikit-tracker/sktracker/data/stack_list/Stack-2.tif',
     '/home/hadim/Insync/Documents/phd/dev/scikit-tracker/sktracker/data/stack_list/Stack-3.tif',
     '/home/hadim/Insync/Documents/phd/dev/scikit-tracker/sktracker/data/stack_list/Stack-4.tif']



Get sample H5 file stored by ``sktacker.io.ObjectsIO``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    df = pd.HDFStore(data.sample_h5())
    print(df.keys())
    print(df['metadata'])

.. parsed-literal::

    ['/metadata', '/objects']
    Shape             (512, 512, 23, 5)
    SizeT                             5
    FileName             sample.ome.tif
    Type                        unint16
    TimeIncrement                     3
    PysicalSizeX                   0.43
    PysicalSizeY                   0.43
    DimensionOrder                 TZYX
    SizeZ                            23
    SizeX                           512
    SizeY                           512
    PysicalSizeZ                    1.5
    dtype: object


See also : - ``sample_ome()`` - ``tubhiswt_4D()`` - ``stack_list_dir()``
- ``TZ_nucleus`` - ``TC_BF_cells()`` - ``metadata_json()`` -
``sample_h5_temp()`` - ``brownian_trajs_df()`` -
``directed_motion_trajs_df()`` - ``trackmate_xml_temp()`` -
``trackmate_xml()`` - ``with_gaps_d()``

Available in the API references.

.. code:: python

    # Run this cell first.
    %load_ext autoreload
    %autoreload 2