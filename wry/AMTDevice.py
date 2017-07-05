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

import common
import exceptions
import pywsman
import AMTBoot
import AMTPower
import AMTKVM
import AMTOptIn
import AMTRedirection
from wry.data_structures import WryDict
import config

'''
Created on 4 Jul 2017

@author: adrian
'''

class AMTDevice(object):
    '''A wrapper class which packages AMT functionality into an accessible, device-centric format.'''

    def __init__(self, location, protocol, username, password):
        port = common.AMT_PROTOCOL_PORT_MAP[protocol]
        path = '/wsman'
        self.client = pywsman.Client(location, port, path, protocol, username, password)
        self.options = pywsman.ClientOptions()

        self.boot = AMTBoot.AMTBoot(self.client, self.options)
        self.power = AMTPower.AMTPower(self.client, self.options)
        self.kvm = AMTKVM.AMTKVM(self.client, self.options)
        self.opt_in = AMTOptIn.AMTOptIn(self.client, self.options)
        self.redirection = AMTRedirection.AMTRedirection(self.client, self.options)

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

    def get_resource(self, resource_name, as_xmldoc=False):
        '''
        Get a native representaiton of a resource, by name. The resource URI will be
        sourced from config.RESOURCE_URIs
        '''
        return common.get_resource(self.client, resource_name, options=self.options, as_xmldoc=as_xmldoc)

    def enumerate_resource(self, resource_name): # Add in all relevant kwargs...
        '''
        Get a native representaiton of a resource, and its instances. The
        resource URI will be sourced from config.RESOURCE_URIs
        '''
        return common.enumerate_resource(self.client, resource_name)

    def put_resource(self, data, uri=None, silent=False):
        '''
        Given a WryDict describing a resource, put this data to the client.
        '''
        return common.put_resource(self.client, data, uri, options=self.options, silent=silent)

    def dump(self, as_json=True):
        '''
        Print all of the known information about the device.

        :returns: WryDict or json.
        '''
        output = WryDict()
        impossible = []
        for name, methods in config.RESOURCE_METHODS.items():
            try:
                if 'get' in methods:
                    resource = self.get_resource(name)
                elif 'enumerate' in methods:
                    resource = self.enumerate_resource(name)
                else:
                    raise exceptions.NoSupportedMethods('The resource %r does not define a supported method for this action.' % name)
            except exceptions.WSManFault:
                impossible.append(name)
            else:
                output.update(resource)
        messages = ['# Could not dump %s' % name for name in impossible]
        if as_json:
            return '\n'.join(messages) + '\n' + output.as_json()
        else:
            print '\n'.join(messages)
            return output

#    def load(self, input_dict):
#        return common.load_from_dict(client, input_dict)
