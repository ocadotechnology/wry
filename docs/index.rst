.. Wry documentation master file, created by
   sphinx-quickstart on Wed May 20 17:21:30 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Wry
===

A Pythonic AMT provisioning, configuration and management library.

It is [very] loosely based on the OpenStack Ironic project, hence the name.

OK, but what is AMT?
--------------------

Intel AMT is a remote management technology, widely implemented in modern Intel
chipsets, and often advertised under the 'vPro' marketing tag.

It provides functionality such as:

- Remote power control
- Remote control via Serial-over-LAN and VNC
- Packet filtering
- Arbitary key/value data storage in NVRAM

AMT is implemented in BMC firmware and is, thus, operating-system independent.

See [Wikipedia](https://en.wikipedia.org/wiki/Intel_Active_Management_Technology) for more information.

.. toctree::
   :maxdepth: 2

   introduction
   usage


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

