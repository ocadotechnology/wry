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

from . import wsmanModule

AMT_KVM_ENABLEMENT_MAP = {
    2: (True, 'Enabled In Use'),
    6: (True, 'Enabled'),
    3: (False, 'Disabled'),
}


class AMTKVM(wsmanModule.wsmanModule):
    '''Control over a device's KVM (VNC) functionality.'''
    _RESOURCES = {
        'kvmRedirectionSap': 'CIM_KVMRedirectionSAP',
        'kvmRedirectionSettingData': 'IPS_KVMRedirectionSettingData',
        'redirectionService': 'AMT_RedirectionService',
        'tlsSettingData': 'AMT_TLSSettingData',
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

    @property
    def enabled_ports(self):
        '''Tells you (and/or allows you to set) the enabled ports for VNC.'''
        ports = set()
        if self.RESOURCES['kvmRedirectionSettingData'].get('Is5900PortEnabled'):
            ports.add(5900)
        if self.RESOURCES['redirectionService'].get('ListenerEnabled'):
            ports.add(16994)
            if self.RESOURCES['tlsSettingData'].enumerate()['AMT_TLSSettingData'][0]['Enabled']:
                ports.add(16995)
        return ports

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
