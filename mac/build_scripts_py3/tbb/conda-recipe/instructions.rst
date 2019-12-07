To build a conda package to the following:

.. code-block:: console

    cd <dir_containing_conda_recipe>

From base conda environment run:

.. code-block:: console

    conda-build  . --python=3.7

Your package will be built in ``<conda_installation_dir>/conda-bld/noarch``

Then repeat with

.. code-block:: console

    conda-build  . --python=3.7

and so on for all python versions you plan on supporting

To install just-built conda package create conda environment (or use existing one) and run:

.. code-block:: console

    conda install <your package name> -c local


To clean up after multiple installs go to ``<conda_installation_dir>/conda-bld`` and remove
all directories that begin with ``pipeline_common_xxxxx`` where ``xxxx`` denotes stamp that conda
gives to each work directory it creates or run

.. code-block:: console

    conda build purge-all

Remarks
-------

When your build does not include platform specific code - think SWIG C/C++ extensions dll, so etc
then putting

.. code-block:: python

    build:
      noarch: generic

In the ``meta.yaml`` is a good strategy.

Otherwise comment ``noarch:generic`` line and build platform-specific package

Useful documentation:
https://docs.conda.io/projects/conda-build/en/latest/user-guide/tutorials/building-conda-packages.html#building-with-a-python-version-different-from-your-miniconda-installation

https://conda.io/projects/conda-build/en/latest/resources/commands/index.html



