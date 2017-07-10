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

import wsmanModule

'''
Created on 5 Jul 2017

@author: adrian
'''


CONSENT_MAPPING = {
    0: None,
    1: 'KVM',
    4294967295: 'All',
}


OPT_IN_STATE = {
    0: 'Not started',
    1: 'Requested',
    2: 'Displayed',
    3: 'Received',
    4: 'In Session',
}


class AMTOptIn(wsmanModule.wsmanModule):
    '''Manage user consent and opt-in codes.'''
    RESOURCES = {
        'optInService': 'IPS_OptInService',
    }

    @property
    def required(self):
        return CONSENT_MAPPING[self.RESOURCES['optInService'].get('OptInRequired')]

    @required.setter
    def required(self, value):
        for key, val in self.CONSENT_MAPPING.items():
            if value == val:
                self.RESOURCES['optInService'].put(OptInRequired = key)
                return
        else:
            raise KeyError


    @property
    def code_ttl(self):
        '''How long an opt-in code lasts, in seconds.'''
        return self.RESOURCES['optInService'].get('OptInCodeTimeout')

    @code_ttl.setter
    def code_ttl(self, value):
        if type(value) != int or value < 60 or value > 900:
            raise TypeError('TTL (in seconds) must be an integer between 60 and 900.')
        self.RESOURCES['optInService'].put(OptInCodeTimeout = value)

    @property
    def state(self):
        return OPT_IN_STATE[self.RESOURCES['optInService'].get('OptInState')]
