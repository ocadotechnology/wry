# Wry

Wry is a Pythonic AMT provisioning, configuration and management library.

It is [very] loosely based on the OpenStack Ironic project.

## Quickstart

Wry's functionality is exposed through the AMTDevice class. Initialize it as such:

    >>> from wry import AMTDevice
    >>> dev = AMTDevice(address, 'http', username, password)

You can then access different apects of device functionality, through aspect-specific namespaces. For example:

    >>> dev.power.turn_on()
    >>> dev.power.state
    StateMap(state='on', sub_state=None)

## Status
Wry is in the early stages of development, and the interfaces it exposes may change as a result. Issues and pull requests are more than welcome.

Wry currently supports only Python 2.7. There are no philosophical reasons for this; it simply matches our target environment. Patches to support other platforms are welcome.

## Compatibility

Wry relies on the wsman AMT protocol, and therefore supports AMT versions 7(?) onwards.

Tested on the following hardware/firmware:

- Intel NUC DC53427HYE (BIOS 0037, ME 8.1.40.1416)
- Intel NUC5i5MYBE

## License

Apache 2.0. (C) 2015 Ocado Innovation Ltd. Please see the `LICENSE` and `NOTICE` files.

