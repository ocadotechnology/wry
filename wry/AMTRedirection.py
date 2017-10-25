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

AMT_REDIRECTION_STATE_MAP = {
    0: 'Unknown',
    1: 'Other',
    2: 'Enabled',
    3: 'Disabled',
    4: 'Shutting Down',
    5: 'Not Applicable',
    6: 'Enabled but Offline',
    7: 'In Test',
    8: 'Deferred',
    9: 'Quiesce',
    10: 'Starting',
    11: 'DMTF Reserved',
    32768: (),
    32769: ('IDER'),
    32770: ('SoL'),
    32771: ('IDER', 'SoL'),
}


class AMTRedirection(wsmanModule.wsmanModule):
    '''Control over Serial-over-LAN and storage redirection.'''
    _RESOURCES = {
        'redirectionService': 'AMT_RedirectionService',
    }

    @property
    def enabled_features(self):
        state = self.RESOURCES['redirectionService'].get('EnabledState')
        return AMT_REDIRECTION_STATE_MAP[state]

    @enabled_features.setter
    def enabled_features(self, features):
        if not features:
            value = 32768
        elif 'SoL' in features and 'IDER' in features:
            value = 32771
        elif 'SoL' in features:
            value = 32770
        elif 'IDER' in features:
            value = 32769
        else:
            raise ValueError('Invalid data provided. Please provide a list comprising only of the following elements: %s' % ', '.join([value.__repr__ for value in self.enabled.values]))
        self.RESOURCES['redirectionService'].put(EnabledState = value)
