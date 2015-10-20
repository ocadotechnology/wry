Wry's functionality is exposed through the AMTDevice class. Initialize it as such:

.. code:: python

    >>> from wry import AMTDevice
    >>> dev = AMTDevice 

You can then access different apects of device functionality, through aspect-specific namespaces. For example:

.. code:: python

    >>> dev.power.turn_on()
    >>> dev.power.state
    StateMap(state='on', sub_state=None)

Currently, the following namespaces are implemented:

    - dev.power, via :class:`wry.device.AMTPower`
    - dev.kvm, via :class:`wry.device.AMTKVM`
    - dev.boot, via :class:`wry.device.AMTBoot`

You can click on a class name above, to see documentation for the available methods.
