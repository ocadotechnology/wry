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

import AMTBoot
import AMTPower
import AMTKVM
import AMTOptIn
import AMTRedirection
import AMTEthernet
import wsmanData
import WryDict
import wsmanResource

'''
Created on 4 Jul 2017

@author: adrian
'''

class AMTDevice(object):
    '''A wrapper class which packages AMT functionality into an accessible, device-centric format.'''

    def __init__(self, target = None, is_ssl = True, username = None, password = None, debug = False, showxml = False):
        '''
        Create the separate resource classes

        @param target: the hostname or IP address of the wsman service
        @param is_ssl: should we communicate using SSL?
        @param username: the username to log in with
        @param password: the password to log in with
        '''
        self._debug = debug
        self._showxml = showxml
        # Stash the settings everyone will need
        self.target = target
        self.is_ssl = is_ssl
        self.username = username
        self.password = password
        # Now create the resource classes
        self.boot = AMTBoot.AMTBoot(self)
        self.power = AMTPower.AMTPower(self)
        self.kvm = AMTKVM.AMTKVM(self)
        self.opt_in = AMTOptIn.AMTOptIn(self)
        self.redirection = AMTRedirection.AMTRedirection(self)
        self.eth = AMTEthernet.AMTEthernet(self)

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug):
        self._debug = debug
        self.boot.debug = debug
        self.power.debug = debug
        self.kvm.debug = debug
        self.opt_in.debug = debug
        self.redirection.debug = debug

    @property
    def showxml(self):
        return self._showxml

    @showxml.setter
    def showxml(self, showxml):
        self._showxml = showxml
        self.boot.showxml = showxml
        self.power.showxml = showxml
        self.kvm.showxml = showxml
        self.opt_in.showxml = showxml
        self.redirection.showxml = showxml

    def dump(self, as_json = True):
        '''
        Print all of the known information about the device.

        :returns: WryDict or json.
        '''
        output = WryDict.WryDict()
        impossible = []
        for name, methods in wsmanData.RESOURCE_METHODS.items():
            try:
                res = wsmanResource.wsmanResource(
                    target = self.target,
                    is_ssl = self.is_ssl,
                    username = self.username,
                    password = self.password,
                    resource = name,
                    debug = self.debug,
                    showxml = self.showxml,
                )
                methods = methods.keys()
                if 'enumerate' in methods:
                    resource = res.enumerate()
                elif 'get' in methods:
                    resource = res.get()
                else:
                    raise NotImplementedError('The resource %r does not define a supported method for this action.' % name)
            except:
                impossible.append(name)
            else:
                output.update(resource)
        messages = ['# Could not dump %s' % name for name in impossible]
        if as_json:
            return '\n'.join(messages) + '\n' + output.as_json()
        print '\n'.join(messages)
        return output
