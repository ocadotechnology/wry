#!/usr/bin/env python2

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import wsman

'''
Created on 4 Jul 2017

@author: adrian
'''

AMT_POWER_STATE_MAP = {
    0:  (None, None),
    1:  ('other', None),
    2:  ('on', None),
    3:  ('sleep', 'Light'),
    4:  ('sleep', 'Deep'),
    5:  ('cycle', '(Off - Soft)'),
    6:  ('off', 'hard'),
    7:  ('hibernate', '(Off - Soft)'),
    8:  ('off', 'soft'),
    9:  ('cycle', '(Off - Hard)'),
    10: ('Master Bus Reset', None),
    11: ('Diagnostic Interrupt (NMI)', None),
    12: ('off', 'Soft Graceful'),
    13: ('off', 'Hard Graceful'),
    14: ('Master Bus Reset', 'Graceful'),
    15: ('cycle', '(Off - Soft Graceful)'),
    16: ('cycle', '(Off - Hard Graceful)'),
    17: ('Diagnostic Interrupt (INIT)', None),
}


class AMTPower:
    '''Control over a device's power state.'''

    def __init__(self, device):
        self.resource = wsman.wsmanResource(
            target = device.target,
            is_ssl = device.is_ssl,
            username = device.username,
            password = device.password,
            resource = 'CIM_AssociatedPowerManagementService'
        )

    def request_power_state_change(self, power_state):
        '''
        Change the NUC to the specified power state
        '''
        return self.resource.invoke(
            'RequestPowerStateChange',
            headerSelectorType = "Name",
            headerSelector = 'Intel(r) AMT Power Management Service',
            power_state = power_state,
        )

    @property
    def state(self):
        '''
        A property which describes the machine's power state.

        A :class:`wry.device.StateMap` as described in
        :data:`wry.device.AMT_POWER_STATE_MAP`.
        '''
        response = self.get(setting = 'PowerState')
        return AMT_POWER_STATE_MAP[response]

    def turn_on(self):
        '''Turn on the device.'''
        self.request_power_state_change(AMT_POWER_STATE_MAP.index(('on', None)))

    def turn_off(self):
        '''Turn off the device.'''
        return self.request_power_state_change(AMT_POWER_STATE_MAP.index(('off', 'soft')))

    def reset(self):
        '''Reboot the device.'''
        return self.request_power_state_change(AMT_POWER_STATE_MAP.index(('cycle', '(Off - Soft)')))

    def toggle(self):
        """
        If the device is off, turn it on.
        If it is on, turn it off.
        """
        state = self.state[0]
        if state == 'on':
            self.turn_off()
        elif state == 'off':
            self.turn_on()
        else:
            raise NotImplementedError("Unable to toggle from unrecognised state '%s'" % (state,))
