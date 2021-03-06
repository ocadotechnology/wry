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

from . import wsmanModule

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


class AMTPower(wsmanModule.wsmanModule):
    '''Control over a device's power state.'''
    _RESOURCES = {
        'power': 'CIM_PowerManagementService',
        'aux': 'CIM_AssociatedPowerManagementService',
    }

    def request_power_state_change(self, power_state):
        '''
        Change the NUC to the specified power state
        '''
        return self.RESOURCES['power'].invoke(
            'RequestPowerStateChange',
            headerSelectorType = "Name",
            headerSelector = 'Intel(r) AMT Power Management Service',
            power_state = power_state,
        )['RequestPowerStateChange_OUTPUT']['ReturnValue']

    @property
    def state(self):
        '''
        A property which describes the machine's power state.

        A :class:`wry.device.StateMap` as described in
        :data:`wry.device.AMT_POWER_STATE_MAP`.
        '''
        response = int(self.RESOURCES['aux'].get(setting = 'PowerState'))
        return AMT_POWER_STATE_MAP[response][0]

    def turn_on(self):
        '''Turn on the device.'''
        return self.request_power_state_change(2)

    def turn_off(self):
        '''Turn off the device.'''
        return self.request_power_state_change(8)

    def reset(self):
        '''Reboot the device.'''
        return self.request_power_state_change(5)


    def available_states(self):
        '''Get a list of available power states given our current power state'''
        try:
            response = self.RESOURCES['aux'].get(setting = 'AvailableRequestedPowerStates')
            if type(response) != type([]):
                response = [response]
            return response
        except:
            return []

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
