Introduction
------------

Wry is a library that facilitates interaction with, and configuration and control of, hardware devices that implement Intel AMT (vPro) technology.

It uses the openwsman python bindings.

Quickstart
++++++++++

.. include:: quickstart.rst

Status
++++++
Wry is in the early stages of development, and the interfaces it exposes may change as a result. Issues and pull requests are more than welcome.

Wry currently supports only Python 2.7. There are no philosophical reasons for this; it simply matches our target environment. Patches to support other platforms are welcome.

Compatibility
+++++++++++++

Wry relies on the wsman AMT protocol, and therefore supports AMT versions 7(?) onwards.

Tested on the following hardware/firmware:
    - Intel NUC DC53427HYE (BIOS 0037, ME 8.1.40.1416)
    - Intel NUC5i5MYBE

License
+++++++

Apache. (C) 2015 Ocado Innovation Ltd. Please see the :download:`LICENSE <../LICENSE>` and :download:`NOTICE <../NOTICE>` files.

