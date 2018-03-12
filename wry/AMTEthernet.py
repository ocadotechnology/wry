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

class AMTEthernet(wsmanModule.wsmanModule):
    ''' Return details about the device's ethernet port(s) '''
    _RESOURCES = {
        'eth': 'AMT_EthernetPortSettings',
    }

    @property
    def state(self):
        '''
        A property which returns the primary ethernet port settings
        '''
        response = self.RESOURCES['eth'].get()
        return response

    @property
    def mac(self):
        response = self.RESOURCES['eth'].get(setting = 'MACAddress')
        return response
