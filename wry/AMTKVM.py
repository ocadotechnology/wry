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

AMT_KVM_ENABLEMENT_MAP = {
    2: (True, 'Enabled In Use'),
    6: (True, 'Enabled'),
    3: (False, 'Disabled'),
}

class EnablementMap(object):
    '''TODO: Refactor this to just be a dict. It should simplify things a lot.'''
    def __init__(self, *values, **options):
        # Make this take ONE ARRAY of values...
        ''' Might want to stop people providing None.'''
        self.values = values
        self.options = options
        self._enabled_values = []

    def __repr__(self):
        return 'EnablementMap(%s)' % ', '.join(
                ['%s: %s' % (value.__repr__(), value in self.options) for value in self.values]
        )

    def __str__(self):
        return self.__repr__()

    def __iadd__(self, value):
        try:
            self.options['iadd'](value)
        except (KeyError, TypeError):
            raise AttributeError('No iadd function specified.')

    def __isub__(self, value):
        try:
            self.options['isub'](value)
        except (KeyError, TypeError):
            raise AttributeError('No isub function specified.')

    def toggle(self, value):
        if value not in self.values:
            raise TypeError('%r is an invalid value. Choose one of %r.' % (value, self.values))
        try:
            self._enabled_values.remove(value)
        except ValueError:
            self._enabled_values.append(value)

    @property
    def enabled(self):
        return self._enabled_values

    @enabled.setter
    def enabled(self, values):
        to_set = []
        for value in values:
            if value not in self.values:
                raise TypeError('%r is an invalid value. Choose one of %r.' % (value, self.values))
            to_set.append(value)
        self._enabled_values = to_set


class AMTKVM(wsman.wsmanModule):
    '''Control over a device's KVM (VNC) functionality.'''
    RESOURCES = {
        'kvmRedirectionSap': 'CIM_KVMRedirectionSAP',
        'kvmRedirectionSettingData': 'IPS_KVMRedirectionSettingData',
        'redirectionService': 'AMT_RedirectionService',
    }

    @property
    def enabled(self):
        '''
        Whether KVM functionality is enabled or disabled.

        True/False

        .. note:: This will return True even if KVM is enabled, but no ports for it
           are.
        '''
        e_state = self.RESOURCES['kvmRedirectionSap'].get('EnabledState')
        return AMT_KVM_ENABLEMENT_MAP[e_state][0]

    @enabled.setter
    def enabled(self, value):
        if value is True:
            requested_state = 2
        elif value is False:
            requested_state = 3
        else:
            raise TypeError('Please specify Either True or False.')
        self.RESOURCES['kvmRedirectionSap'].invoke(
            'RequestStateChange',
            state = requested_state
        )

#    @property
#    def enabled_ports(self):
#        '''Tells you (and/or allows you to set) the enabled ports for VNC.'''
#
#        def iadd(values):
#            self.enabled_ports = self.enabled_ports.enabled + values
#
#        def isub(values):
#            self.enabled_ports = set(self.enabled_ports.values) - set(values)
#
#        ports = EnablementMap(5900, 16994, 16995, iadd = iadd, isub = isub)
#
#        if self.get('IPS_KVMRedirectionSettingData', 'Is5900PortEnabled'):
#            ports.toggle(5900)
#        if self.get('AMT_RedirectionService', 'ListenerEnabled'):
#            ports.toggle(16994)
#            if self.walk('AMT_TLSSettingData')['AMT_TLSSettingData'][0]['Enabled']:
#                ports.toggle(16995)
#        return ports
#
#    @enabled_ports.setter
#    def enabled_ports(self, values):
#        ports = self.enabled_ports.values
#        enabled = self.enabled_ports.enabled
#        print 'values: ', values
#        print 'ports: ', ports
#        # Validation:
#        invalid = list(set(values) - set(ports))
#        if invalid:
#            raise ValueError('Invalid port(s) specified: %r. Valid ports are %r.'
#                % (invalid, ports))
#        if 16995 in values and 16995 not in enabled:
#            if 16994 not in values:
#                raise ValueError('Port 16995 cannot be enabled unless port 16994 is enabled also.')
#            else:
#                if not self.walk('AMT_TLSSettingData')['AMT_TLSSettingData'][0]['Enabled']:
#                    raise ValueError('Port 16995 can only be set by enabling both TLS and port 16994.')
#        # Setter logic:
#        for port, enable in [(port, port in values) for port in ports]:
#            if (enable and port not in enabled) or (not enable and port in enabled):
#                if port == 5900:
#                    self.put('IPS_KVMRedirectionSettingData', {'Is5900PortEnabled': enable})
#                elif port == 16994:
#                    self.put('AMT_RedirectionService', {'ListenerEnabled': enable})
#                self.enabled_ports.toggle(port)

    @property
    def port_5900_enabled(self):
        '''
        Whether the standard VNC port (5900) is enabled. True/False.
        '''
        return self.RESOURCES['kvmRedirectionSettingData'].get('Is5900PortEnabled')

    @port_5900_enabled.setter
    def port_5900_enabled(self, value):
        return self.RESOURCES['kvmRedirectionSettingData'].put(Is5900PortEnabled = value)

    @property
    def default_screen(self):
        '''
        Default Screen. An integer.
        '''
        return self.RESOURCES['kvmRedirectionSettingData'].get('DefaultScreen')

    @default_screen.setter
    def default_screen(self, value):
        self.RESOURCES['kvmRedirectionSettingData'].put(DefaultScreen = value)

    @property
    def opt_in_timeout(self):
        '''
        User opt-in timeout for KVM access, in seconds.

        If set to 0, opt-in will be disabled.
        '''
        timeout = \
            (not self.RESOURCES['kvmRedirectionSettingData'].get('OptInPolicy')) or \
            self.RESOURCES['kvmRedirectionSettingData'].get('OptInPolicyTimeout')
        if timeout == True:
            return 0
        return timeout

    @opt_in_timeout.setter
    def opt_in_timeout(self, value):
        if not value:
            self.RESOURCES['kvmRedirectionSettingData'].put(
                OptInPolicy = False
            )
        else:
            self.RESOURCES['kvmRedirectionSettingData'].put(
                OptInPolicy = True,
                OptInPolicyTimeout = value,
            )

    @property
    def session_timeout(self):
        '''
        Session timeout. In minutes.
        '''
        return self.RESOURCES['kvmRedirectionSettingData'].get('SessionTimeout')

    @session_timeout.setter
    def session_timeout(self, value):
        return self.RESOURCES['kvmRedirectionSettingData'].put(SessionTimeout = value)

    @property
    def password(self):
        "This doesn't fail but always appears to return None"
        return self.RESOURCES['kvmRedirectionSettingData'].get('RFBPassword')

    @password.setter
    def password(self, value):
        self.RESOURCES['kvmRedirectionSettingData'].put(RFBPassword = value)

    @property
    def consent_required(self):
        return self.RESOURCES['kvmRedirectionSettingData'].get('OptInPolicy')

    @consent_required.setter
    def consent_required(self, value):
        self.RESOURCES['kvmRedirectionSettingData'].put(OptInPolicy = value)

    def setup(self,
              password = '',
              port5900Enabled = False,
              defaultScreen = 0,
              optIn = True,
              optInTimeout = 60,
              sessionTimeout = 10):
        '''
        Set all basic KVM settings in one call
        '''
        self.RESOURCES['kvmRedirectionSettingData'].put(
            Is5900PortEnabled = port5900Enabled,
            DefaultScreen = defaultScreen,
            OptInPolicy = optIn,
            RFBPassword = password,
            OptInPolicyTimeout = optInTimeout,
            SessionTimeout = sessionTimeout,
        )
