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

class AMTBoot(wsmanModule.wsmanModule):
    '''Control how the machine will boot next time.'''

    _RESOURCES = {
        'bootSourceSetting': 'CIM_BootSourceSetting',
        'bootService': 'CIM_BootService',
        'bootSettingData': 'AMT_BootSettingData',
        'bootConfigSetting': 'CIM_BootConfigSetting'
    }

    @property
    def supported_media(self):
        '''Media the device can be configured to boot from.'''
        returned = self.RESOURCES['bootSourceSetting'].enumerate()['CIM_BootSourceSetting']
        return [source['StructuredBootString'].split(':')[-2] for source in returned]

    @property
    def medium(self):
        raise NotImplementedError('It is not currently possible to detect which medium a device will boot from.')

    @medium.setter
    def medium(self, value):
        '''Set boot medium for next boot.'''
        sources = self.RESOURCES['bootSourceSetting'].enumerate()['CIM_BootSourceSetting']
        for source in sources:
            if value in source['StructuredBootString']:
                instance_id = source['InstanceID']
                break
        else:
            raise LookupError('This medium is not supported by the device')

#TODO Should be an enumerate, as it has intances... But for now...
        boot_config = self.RESOURCES['bootConfigSetting'].get()['CIM_BootConfigSetting']
        config_instance = str(boot_config['InstanceID'])

        self.RESOURCES['bootConfigSetting'].invoke(
            'ChangeBootOrder',
            headerSelectorType = "InstanceID",
            headerSelector = config_instance,
            boot_device = instance_id
        )
        self.RESOURCES['bootService'].invoke(
            'SetBootConfigRole',
            headerSelectorType = "Name",
            headerSelector = "Intel(r) AMT Boot Service",
            role = "1",
        )

    @property
    def config(self):
        '''Get configuration for the machine's next boot.'''
        return self.RESOURCES['bootSettingData'].get()
