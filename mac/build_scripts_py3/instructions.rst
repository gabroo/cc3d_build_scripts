all qt run scripts - compucell3d.command and twedit must
define

QT_QPA_PLATFORM_PLUGIN_PATH


.. code-block: bash

    export QT_QPA_PLATFORM_PLUGIN_PATH=${PREFIX_CC3D}/python37/plugins


or else the following erro rwill show up

.. code-block: bash

    This application failed to start because it could not find or load the Qt platform plugin "cocoa"
    in "".

    Reinstalling the application may fix this problem.