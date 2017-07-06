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
'''
Created on 4 Jul 2017

@author: adrian
'''

class AMTBoot(DeviceCapability.DeviceCapability):
    '''Control how the machine will boot next time.'''

    @property
    def supported_media(self):
        '''Media the device can be configured to boot from.'''
        returned = self.walk('CIM_BootSourceSetting')
        return [source['StructuredBootString'].split(':')[-2] for source in returned['CIM_BootSourceSetting']]

    @property
    def medium(self):
        raise NotImplementedError('It is not currently possible to detect which medium a device will boot from.')

    @medium.setter
    def medium(self, value):
        '''Set boot medium for next boot.'''
        sources = self.walk('CIM_BootSourceSetting')['CIM_BootSourceSetting']
        for source in sources:
            if value in source['StructuredBootString']:
                instance_id = source['InstanceID']
                break
        else:
            raise LookupError('This medium is not supported by the device')

        boot_config = self.get('CIM_BootConfigSetting') # Should be an
        # enumerate, as it has intances... But for now...
        config_instance = str(boot_config['InstanceID'])

        common.invoke_method(
            service_name='CIM_BootConfigSetting',
            resource_name='CIM_BootSourceSetting',
            affected_item='Source',
            method_name='ChangeBootOrder',
            options=self.options,
            client=self.client,
            selector=('InstanceID', instance_id, config_instance, ),
        )
        self._set_boot_config_role()

    @property
    def config(self):
        '''Get configuration for the machine's next boot.'''
        return self.get('AMT_BootSettingData')

    def _set_boot_config_role(self, enabled_state=True):
        if enabled_state == True:
            role = '1'
        elif enabled_state == False:
            role = '32768'
        svc = self.get('CIM_BootService')
        assert svc['ElementName'] == 'Intel(r) AMT Boot Service'
        return common.invoke_method(
            service_name='CIM_BootService',
            resource_name='CIM_BootConfigSetting',
            affected_item='BootConfigSetting',
            method_name='SetBootConfigRole',
            options=self.options,
            client=self.client,
            selector=('InstanceID', 'Intel(r) AMT: Boot Configuration 0', ),
            args_after=[('Role', role)],
        )
