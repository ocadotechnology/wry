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
from collections import OrderedDict
from wry.data_structures import RadioButtons

'''
Created on 5 Jul 2017

@author: adrian
'''


class AMTOptIn(DeviceCapability.DeviceCapability):
    '''Manage user consent and opt-in codes.'''

    def __init__(self, *args, **kwargs):
        self._consent_mapping = OrderedDict([
            (0, None),
            (1, 'KVM'),
            (4294967295, 'All'),
        ])
        self._consent_values = RadioButtons(self._consent_mapping.values())
        super(AMTOptIn, self).__init__(*args, **kwargs)

    @property
    def required(self):
        level = self._consent_mapping[self.get('IPS_OptInService', 'OptInRequired')]
        self._consent_values.selected = level
        return self._consent_values

    @required.setter
    def required(self, value):
        for key, val in self._consent_mapping.items():
            if value == val:
                break
        else:
            raise KeyError
        self.put('IPS_OptInService', {'OptInRequired': key})
        self._consent_values.selected = value

    @property
    def code_ttl(self):
        '''How long an opt-in code lasts, in seconds.'''
        return self.get('IPS_OptInService', 'OptInCodeTimeout')

    @code_ttl.setter
    def code_ttl(self, value):
        try:
            assert type(value) == int
            assert 60 <= value <= 900
        except (TypeError, AssertionError):
            raise TypeError('TTL (in seconds) must be an integer between 60 and 900.')
        self.put('IPS_OptInService', {'OptInCodeTimeout': value})

    @property
    def state(self):
        mapping = {
            0: 'Not started',
            1: 'Requested',
            2: 'Displayed',
            3: 'Received',
            4: 'In Session',
        }
        return mapping[self.get('IPS_OptInService', 'OptInState')]
