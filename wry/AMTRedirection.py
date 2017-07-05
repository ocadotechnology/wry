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

from collections import OrderedDict
import DeviceCapability
from wry.AMTKVM import EnablementMap

'''
Created on 5 Jul 2017

@author: adrian
'''


class AMTRedirection(DeviceCapability.DeviceCapability):
    '''Control over Serial-over-LAN and storage redirection.'''

    def __init__(self, *args, **kwargs):
        self._state_mapping = OrderedDict([
            (0, 'Unknown'),
            (1, 'Other'),
            (2, 'Enabled'),
            (3, 'Disabled'),
            (4, 'Shutting Down'),
            (5, 'Not Applicable'),
            (6, 'Enabled but Offline'),
            (7, 'In Test'),
            (8, 'Deferred'),
            (9, 'Quiesce'),
            (10, 'Starting'),
            (11, 'DMTF Reserved'),
            (32768, 'IDER and SOL are disabled'),
            (32769, 'IDER is enabled and SOL is disabled'),
            (32770, 'SOL is enabled and IDER is disabled'),
            (32771, 'IDER and SOL are enabled'),
        ])
        super(AMTRedirection, self).__init__(*args, **kwargs)
    
    @property
    def enabled_features(self):
        items = EnablementMap('SoL', 'IDER')
        state = self.get('AMT_RedirectionService', 'EnabledState')
        if state >= 32768:
            if state in (32769, 32771):
                items.toggle('IDER')
            if state in (32770, 32771):
                items.toggle('SoL')
        else:
            if state in self._state_mapping:
                raise LookupError('Unknown state discovered: %r' % self._state_mapping[state])
            raise KeyError('Unknown state discovered: %r' % state)
        return items

    @enabled_features.setter
    def enabled_features(self, features):
        if not features:
            self.put('AMT_RedirectionService', {'EnabledState': 32768})
        elif set(features) == set(['SoL', 'IDER']):
            self.put('AMT_RedirectionService', {'EnabledState': 32771})
        elif features[0] == 'SoL':
            self.put('AMT_RedirectionService', {'EnabledState': 32770})
        elif features[0] == 'IDER':
            self.put('AMT_RedirectionService', {'EnabledState': 32769})
        else:
            raise ValueError('Invalid data provided. Please provide a list comprising only of the following elements: %s' % ', '.join([value.__repr__ for value in self.enabled.values]))
