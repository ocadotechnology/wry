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
import wsmanData
import WryDict
import wsmanResource

'''
Created on 4 Jul 2017

@author: adrian
'''

class AMTDevice(object):
    '''A wrapper class which packages AMT functionality into an accessible, device-centric format.'''

    def __init__(self, target = None, is_ssl = True, username = None, password = None):
        '''
        Create the separate resource classes

        @param target: the hostname or IP address of the wsman service
        @param is_ssl: should we communicate using SSL?
        @param username: the username to log in with
        @param password: the password to log in with
        '''
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
                    resource = name
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

"""
    @property
    def debug(self):
        '''
        When set to True, openwsman will dump every [#]_ request made to the client.
        '''
        if self.options.get_flags() == 16:
            return True
        return False

    @debug.setter
    def debug(self, value):
        if value:
            self.options.set_dump_request()
        else:
            self.options.clear_dump_request()

    def get_resource(self, resource_name, as_xmldoc = False):
        '''
        Get a native representaiton of a resource, by name. The resource URI will be
        sourced from config.RESOURCE_URIS
        '''
        return common.get_resource(self.client, resource_name, options = self.options, as_xmldoc = as_xmldoc)

    def enumerate_resource(self, resource_name): # Add in all relevant kwargs...
        '''
        Get a native representaiton of a resource, and its instances. The
        resource URI will be sourced from config.RESOURCE_URIS
        '''
        return common.enumerate_resource(self.client, resource_name)

    def put_resource(self, data, uri = None, silent = False):
        '''
        Given a WryDict describing a resource, put this data to the client.
        '''
        return common.put_resource(self.client, data, uri, options = self.options, silent = silent)

#    def load(self, input_dict):
#        return common.load_from_dict(client, input_dict)
"""
