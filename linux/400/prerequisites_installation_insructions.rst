Creating your  new python virtual environment aka conda environment:

.. code-block:: console

  conda create -n cc3d_2020 python=3.7

After the environment ``cc3d_2020`` is created we will activate it. BTW you can call this environment whatever you want. Just
Keep the names meaningful to you


.. code-block:: console

  source activate cc3d_2020

Let's install numpy inside this environment because we will need it for the CC3D compilation:

.. code-block:: console

    conda install -c conda-forge numpy scipy pandas jinja2 webcolors vtk=8.2 pyqt pyqtgraph deprecated qscintilla2 jinja2 chardet

We will use ``pip`` to install ``webcolors`` and ``libroadrunner``

.. code-block:: console

    pip install webcolors
    pip install libroadrunner


Most of linux dependencies can be easily installed using conda
the list of installed packages is stored in ``cc3d_2020_env.txt``.

To build this list of exact packages in my conda repository I used the following command

.. code-block:: console

    conda list --explicit > cc3d_2020_env.txt

You may use ``cc3d_2020_env`` to restore exact packages we installed using the following command

.. code-block:: console

    conda create --name cc3d_2020 --file cc3d_2020_env

This command is not always guaranteed to succeed because conda dependencies are often removed from servers making
this method of freezing dependencies unreliable.

More information about conda can be found on

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

Adding TBB to conda environment
-------------------------------

TBB is s C library so all we need to do is to grab binaries for windows from

https://github.com/intel/tbb/blob/master/download.md

For our purposes we used this direct link to grab pre-build windows tbb libraries

https://www.threadingbuildingblocks.org/sites/default/files/software_releases/windows/tbb43_20150611oss_lin.zip

Assuming we are building 64-bit application we copy

``include/tbb`` directory of the tbb binaries into ``<conda_root>/envs/cc3d_2020/Library/include/vtk-8.2`` .


In your case the exact location of conda environment you are creating mught be different . The important part is to go
from the root of the environment - in my case ``<conda_root>/envs/cc3d_2020`` to ``Library/include/vtk-8.2``.

Next we copy make a soft link to existing tbb.so.2 library by running

.. code-block:: console

    cd <conda_root>/envs/cc3d_2020/lib
    ln -s libtbb.so.2 libtbb.so
