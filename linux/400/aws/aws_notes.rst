For general instructions p[lease checkout this link.

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html

In this writeup we will show how to setup CC3D on already existing AWS Ubuntu 18.04 image

We are assuming that we are connecting from a Linux machine.


setting up private key
-----------------------

After generating AWS keys during AWS instance creation we save them in a secure folder, ideally, ``~./ssh`
on local machine. Next, we change private key to have file permissions set to  400

.. code-block:: console

    chmod 400 <path_to_private_key>

connect
-------

To connect to AWS instance without X11 forwarding (e.g. right after creating AWS instance) use the following:

.. code-block:: console

    ssh -i <full path to private key for a given instance> ec2-3-135-208-xxx.us-east-2.compute.amazonaws.com

the ec2-3-135-208-xxx.us-east-2.compute.amazonaws.com can be found on the instance page

Installations
-------------

After initial login run

.. code-block:: console

    sudo apt-get update

This will fetch ubuntu packages so that you can install some on your system

then you can install all the stuff you want to

Install CC3D
------------

On AWS image with ubuntu 18.04 we do the following:

We first install ``xterm`` to make sure we can forward X11 windows

.. code-block:: console

    sudo apt-get install xterm

This single command will install all dependencies needed to forward X11 windows

Next, we disconnect and connect again to  to AWS instance but this time we will request  X11 window forwarding
so that we can see and interact with GUI's

.. code-block:: console

    ssh -X -i <full path to private key for a given instance> ec2-3-135-208-xxx.us-east-2.compute.amazonaws.com

Notice ``-X`` switch that enables X11 window forwarding

.. code-block:: console

    wget wget https://sourceforge.net/projects/cc3d/files/4.2.0/linux/Ubuntu_18.04_64bit/CC3D_4.2.0_ubuntu_18.04_64bit.tar.gz

once the download finishes we install it as follows:

.. code-block:: console

    tar -xvf CC3D_4.2.0_ubuntu_18.04_64bit.tar.gz
