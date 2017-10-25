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

import wsmanResource

class wsmanModule(object):
    '''
    Base class for all wry modules
    '''
    _RESOURCES = {
    }

    def __init__(self, device):
        '''
        Create resources for each defined resource
        '''
        self.RESOURCES = {}
        self._debug = device.debug
        for k in self._RESOURCES.keys():
            self.RESOURCES[k] = wsmanResource.wsmanResource(
                target = device.target,
                is_ssl = device.is_ssl,
                username = device.username,
                password = device.password,
                resource = self._RESOURCES[k],
                debug = device.debug,
                showxml = device.showxml,
            )

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug):
        self._debug = debug
        for k in self.RESOURCES.keys():
            self.RESOURCES[k].debug = debug

    @property
    def showxml(self):
        return self._showxml

    @showxml.setter
    def showxml(self, showxml):
        self._showxml = showxml
