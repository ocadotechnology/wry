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

import DeviceCapability
import common
import config

'''
Created on 4 Jul 2017

@author: adrian
'''

AMT_POWER_STATE_MAP = [
    None,
    config.StateMap('other', None),
    config.StateMap('on', None),
    config.StateMap('sleep', 'Light'),
    config.StateMap('sleep', 'Deep'),
    config.StateMap('cycle', '(Off - Soft)'),
    config.StateMap('off', 'hard'),
    config.StateMap('hibernate', '(Off - Soft)'),
    config.StateMap('off', 'soft'),
    config.StateMap('cycle', '(Off - Hard)'),
    config.StateMap('Master Bus Reset', None),
    config.StateMap('Diagnostic Interrupt (NMI)', None),
    config.StateMap('off', 'Soft Graceful'),
    config.StateMap('off', 'Hard Graceful'),
    config.StateMap('Master Bus Reset', 'Graceful'),
    config.StateMap('cycle', '(Off - Soft Graceful)'),
    config.StateMap('cycle', '(Off - Hard Graceful)'),
    config.StateMap('Diagnostic Interrupt (INIT)', None),
]

'''
.. _CIM\_AssociatedPowerManagementService: http://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/default.htm?turl=HTMLDocuments%2FWS-Management_Class_Reference%2FCIM_BootConfigSetting.htm

Mapping of device power states. A StateMap's index in this list, is the
PowerState value as specified in the CIM\_AssociatedPowerManagementService_
schema class.
'''

class AMTPower(DeviceCapability.DeviceCapability):
    '''Control over a device's power state.'''

    def __init__(self, *args, **kwargs):
        self.resource_name = 'CIM_AssociatedPowerManagementService'
        super(AMTPower, self).__init__(*args, **kwargs)

    def request_power_state_change(self, power_state):
        return common.invoke_method(
            service_name = 'CIM_PowerManagementService',
            resource_name = 'CIM_ComputerSystem',
            affected_item = 'ManagedElement',
            method_name = 'RequestPowerStateChange',
            options = self.options,
            client = self.client,
            selector = ('Name', 'ManagedSystem', 'Intel(r) AMT Power Management Service',),
            args_before = [('PowerState', str(power_state)), ],
            anonymous = True,
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
        sub_state = None
        index = AMT_POWER_STATE_MAP.index(('on', sub_state))
        self.request_power_state_change(index)

    def turn_off(self):
        '''Turn off the device.'''
        return self.request_power_state_change(8)

    def reset(self):
        '''Reboot the device.'''
        return self.request_power_state_change(5)

    def toggle(self):
        """
        If the device is off, turn it on.
        If it is on, turn it off.
        """
        state = self.state
        if state == 'on':
            self.turn_off()
        elif state == 'off':
            self.turn_on()
        else:
            raise NotImplementedError("Unable to toggle from unrecognised state '%s'" % (state,))
