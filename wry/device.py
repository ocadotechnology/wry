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


import pywsman
import json
from collections import namedtuple
from collections import OrderedDict
from wry import common
from wry.data_structures import WryDict
from wry import common
from wry import exceptions
from wry.config import RESOURCE_METHODS, RESOURCE_URIs, SCHEMAS



StateMap = namedtuple('StateMap', ['state', 'sub_state'])


AMT_KVM_ENABLEMENT_MAP = {
    2: StateMap(True, 'Enabled'),
    6: StateMap(True, 'Enabled But Offline'),
    3: StateMap(False, 'Disabled'),
}


AMT_POWER_STATE_MAP = [
    None,
    StateMap('other', None),
    StateMap('on', None),
    StateMap('sleep', 'Light'),
    StateMap('sleep', 'Deep'),
    StateMap('cycle', '(Off - Soft)'),
    StateMap('off', 'hard'),
    StateMap('hibernate', '(Off - Soft)'),
    StateMap('off', 'soft'),
    StateMap('cycle', '(Off - Hard)'),
    StateMap('Master Bus Reset', None),
    StateMap('Diagnostic Interrupt (NMI)', None),
    StateMap('off', 'Soft Graceful'),
    StateMap('off', 'Hard Graceful'),
    StateMap('Master Bus Reset', 'Graceful'),
    StateMap('cycle', '(Off - Soft Graceful)'),
    StateMap('cycle', '(Off - Hard Graceful)'),
    StateMap('Diagnostic Interrupt (INIT)', None),
]
'''
.. _CIM\_AssociatedPowerManagementService: http://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/default.htm?turl=HTMLDocuments%2FWS-Management_Class_Reference%2FCIM_BootConfigSetting.htm

Mapping of device power states. A StateMap's index in this list, is the
PowerState value as specified in the CIM\_AssociatedPowerManagementService_
schema class.
'''


class AMTDevice(object):
    '''A wrapper class which packages AMT functionality into an accessible, device-centric format.'''

    def __init__(self, location, protocol, username, password):
        port = common.AMT_PROTOCOL_PORT_MAP[protocol]
        path = '/wsman'
        self.client = pywsman.Client(location, port, path, protocol, username, password)
        self.options = pywsman.ClientOptions()

        self.power = AMTPower(self.client, self.options)
        self.kvm = AMTKVM(self.client, self.options)

    @property
    def debug(self):
        '''
        When set to True, openwsman will dump every [#]_ request made to the
        client.

        Unfortunately, openwsman does not expose this value, so it only possible
        to set this property, and not to retrieve it.

        .. [#] Actually, every request that makes use of self.options.
        '''
        raise NotImplemented('There is no way to get the value of this property. Please set it explicitly.')
        return self.options.get_dump_request()
    @debug.setter
    def debug(self, value):
        if value:
            self.options.set_dump_request()
        else:
            self.options.clear_dump_request()

    def get_resource(self, resource_name):
        '''
        Get a native representaiton of a resource, by name. The resource URI will be
        sourced from config.RESOURCE_URIs
        '''
        return common.get_resource(self.client, resource_name, options=self.options)

    def enumerate_resource(self, resource_name): # Add in all relevant kwargs...
        '''
        Get a native representaiton of a resource, and its instances. The
        resource URI will be sourced from config.RESOURCE_URIs
        '''
        return common.enumerate_resource(self.client, resource_name)

    def put_resource(self, data, uri=None, silent=False):
        '''
        Given a WryDict describing a resource, put this data to the client.
        '''
        return common.put_resource(self.client, data, uri, options=self.options, silent=silent)

    def dump(self, as_json=True):
        '''
        Print all of the known information about the device.

        :returns: WryDict or json.
        '''
        output = WryDict()
        impossible = []
        for name, methods in RESOURCE_METHODS.items():
            try:
                if 'get' in methods:
                    resource = self.get_resource(name)
                elif 'enumerate' in methods:
                    resource = self.enumerate_resource(name)
                else:
                    raise exceptions.NoSupportedMethods('The resource %r does not define a supported method for this action.' % name)
            except exceptions.WSManFault:
                impossible.append(name)
            else:
                output.update(resource)
        messages = ['# Could not dump %s' % name for name in impossible]
        if as_json:
            return '\n'.join(messages) + '\n' + json.dumps(output, indent=4)
        else:
            print '\n'.join(messages)
            return output

    def load(self, input_dict):
        return common.load_from_dict(client, input_dict)


class DeviceCapability(object):
    '''self.resource_name should be set on the subclass if needed.'''

    def __init__(self, client, options=None):
        self.client = client
        self.options = options

    def get(self, resource_name=None, setting=None):
        if not resource_name:
            resource_name = self.resource_name
        resource = common.get_resource(self.client, resource_name, options=self.options)
        if setting:
            return resource[resource_name][setting]
        return resource[resource_name]

    def put(self, resource_name=None, input_dict=None, silent=False, as_update=True):
        if not resource_name:
            resource_name = self.resource_name
        if as_update:
            resource = common.get_resource(self.client, resource_name, options=self.options)
            resource[resource_name].update(input_dict)
        else:
            resource = WryDict({resource_name: input_dict})
        response = common.put_resource(self.client, resource, silent=silent, options=self.options)
        print response


class AMTPower(DeviceCapability):
    '''Control over a device's power state.'''

    def __init__(self, *args, **kwargs):
        self.resource_name = 'CIM_AssociatedPowerManagementService'
        super(AMTPower, self).__init__(*args, **kwargs)

    def request_power_state_change(self, power_state): 
        resource_name = 'CIM_PowerManagementService'
        input_dict = {  
            resource_name: {
                'RequestPowerStateChange_INPUT': {
                    'PowerState': power_state,
                    'ManagedElement': OrderedDict([
                        ('Address', {
                            '#text': SCHEMAS['addressing_anonymous'],
                            '@xmlns': SCHEMAS['addressing'],
                        }),  
                        ('ReferenceParameters', {      
                            'ResourceURI': {    
                                '#text': RESOURCE_URIs['CIM_ComputerSystem'],
                                '@xmlns': SCHEMAS['wsman'],
                            },
                            '@xmlns': SCHEMAS['addressing'],
                            'SelectorSet': {    
                                'Selector': {       
                                    '#text': 'ManagedSystem',
                                    '@Name': 'Name',
                                },
                                '@xmlns': SCHEMAS['wsman'],
                            },
                        }),
                    ]),
                },  
            }
        }    
        self.options.add_selector('Name', 'Intel(r) AMT Power Management Service') # possible to work on a copy of this?
        response = common.invoke_method(self.client, 'RequestPowerStateChange', input_dict, options=self.options)
        return not response['RequestPowerStateChange_OUTPUT']['ReturnValue']

    @property
    def state(self):
        '''
        A property which describes the machine's power state.
        
        A :class:`wry.device.StateMap` as described in
        :data:`wry.device.AMT_POWER_STATE_MAP`.
        '''
        response = self.get(setting='PowerState')
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
            raise SomeError


class AMTKVM(DeviceCapability):
    '''Control over a device's KVM (VNC) functionality.'''

    def request_state_change(self, resource_name, requested_state):
        input_dict = {
            resource_name:
                {'RequestStateChange_INPUT': {
                    'RequestedState': requested_state,
                },
            }
        }
        return common.invoke_method(self.client, 'RequestStateChange', input_dict, options=self.options)

    @property
    def enabled(self):
        '''
        Whether KVM functionality is enabled or disabled.

        True/False

        .. note:: This will return True even if KVM is enabled, but no ports for it
           are.
        '''
        e_state = self.get('CIM_KVMRedirectionSAP', 'EnabledState')
        return AMT_KVM_ENABLEMENT_MAP[e_state].state
    @enabled.setter
    def enabled(self, value):
        if value is True:
            self.request_state_change('CIM_KVMRedirectionSAP', 2)
        elif value is False:
            self.request_state_change('CIM_KVMRedirectionSAP', 3)
        else:
            raise TypeError('Please specify Either True or False.')

    @property
    def enabled_ports(self):
        raise NotImplemented

    @property
    def port_5900_enabled(self):
        '''
        Whether the standard VNC port (5900) is enabled. True/False.
        '''
        return self.get('IPS_KVMRedirectionSettingData', 'Is5900PortEnabled')
    @port_5900_enabled.setter
    def port_5900_enabled(self, value):
        return self.put('IPS_KVMRedirectionSettingData', {'Is5900PortEnabled': value})

    @property
    def default_screen(self):
        '''
        Default Screen. An integer.
        '''
        return self.get('IPS_KVMRedirectionSettingData', 'DefaultScreen')
    @default_screen.setter
    def default_screen(self, value):
         return self.put({'DefaultScreen': value})

    @property
    def opt_in_timeout(self):
        '''
        User opt-in timeout for KVM access, in seconds.

        If set to 0, opt-in will be disabled.
        '''
        timeout = (not self.get('IPS_KVMRedirectionSettingData', 'OptInPolicy')) or self.get('IPS_KVMRedirectionSettingData', 'OptInPolicyTimeout')
        if timeout == True: # This is NOT READABLE...
            return 0
        return timeout
        # Would be nice to have a way to get multiple values without querying
        # twice...
    @opt_in_timeout.setter
    def opt_in_timeout(self, value):
        if not value:
             return self.put({'OptInPolicy': False})
        else:
             return self.put({'OptInPolicy': True, 'OptInPolicyTimeout': value})

    @property
    def session_timeout(self):
        '''
        Session timeout. An integer.
        '''
        return self.get('IPS_KVMRedirectionSettingData', 'SessionTimeout')
    @session_timeout.setter
    def session_timeout(self, value):
        return self.put({'SessionTimeout': value})

    def password(self, password=None):
        raise NotImplemented
