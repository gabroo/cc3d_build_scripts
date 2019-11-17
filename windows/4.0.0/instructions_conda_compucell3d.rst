Preparing dependencies
----------------------

Most of windows dependencies can be easily installed using conda from compucell3d channel

However if you install the following packages in your newly created conda environment you should be fine

.. code-block:: console

    conda create -n cc3d_test

then

.. code-block:: console

    conda activate cc3d_test


.. code-block:: console

    conda install -c compucell3d vtk=8.2 scipy numpy=1.15 pandas jinja2 pyqt qscintilla2 webcolors pyqtgraph deprecated pywin32 chardet swig=3

    conda install -c compucell3d tbb_full_dev
