Wry
===

Wry is a Pythonic AMT provisioning, configuration and management library.

It is [very] loosely based on the OpenStack Ironic project.

Quickstart
++++++++++

Wry's functionality is exposed through the AMTDevice class. Initialize it as such:

    >>> from wry import AMTDevice
    >>> dev = AMTDevice

You can then access different apects of device functionality, through aspect-specific namespaces. For example:

    >>> dev.power.turn_on()
    >>> dev.power.state
    StateMap(state='on', sub_state=None)

