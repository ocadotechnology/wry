Wry's functionality is exposed through the AMTDevice class. Initialize it as such:

.. code:: python

    >>> from wry import AMTDevice
    >>> dev = AMTDevice.AMTDevice(address, False, username, password)

You can then access different aspects of device functionality, through aspect-specific namespaces. For example:

.. code:: python

    >>> dev.power.turn_on()
    >>> dev.power.state
    StateMap(state='on', sub_state=None)

Currently, the following namespaces are implemented:

    - dev.power, via :class:`wry.AMTPower.AMTPower`, provides access to:

      - Power state and control

    - dev.boot, via :class:`wry.AMTBoot.AMTBoot`, provides access to:

      - Boot configuration
      - Boot medium selection

    - dev.vnc, via :class:`wry.AMTKVM.AMTKVM`, provides access to:

      - Remote KVM (VNC) state and configuration
      - Setting of [additonal] user opt-in policy for KVM

    - dev.opt_in, via :class:`wry.AMTOptIn.AMTOptIn`, provides access to:

      - Setting of opt-in policies for KVM, Serial-over-LAN and media redirection

    - dev.redirection, via :class:`wry.AMTRedirection.AMTRedirection`, provides access to:

      - State and control of media redirection (IDER)
      - State and control of Serial-over-LAN (SOL)

You can click on a class name above, to see documentation for the available methods.
