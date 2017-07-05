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
from wry.data_structures import WryDict

'''
Created on 4 Jul 2017

@author: adrian
'''

class DeviceCapability(object):
    '''self.resource_name should be set on the subclass if needed.'''

    def __init__(self, client, options=None):
        self.client = client
        self.options = options

    def get(self, resource_name=None, setting=None):
        if not resource_name:
            resource_name = self.resource_name
        resource = common.get_resource(self.client, resource_name, options=self.options)
        if setting:
            return resource[resource_name][setting]
        return resource[resource_name]

    def put(self, resource_name=None, input_dict=None, silent=False,
        as_update=True): # Ideally want keyword-only args or a refactor here.
                         # Want to be able to supply only input_dict...
        if not resource_name:
            resource_name = self.resource_name
        if as_update:
            resource = common.get_resource(self.client, resource_name, options=self.options)
            resource[resource_name].update(input_dict)
        else:
            resource = WryDict({resource_name: input_dict})
        response = common.put_resource(self.client, resource, silent=silent, options=self.options)

    def walk(self, resource_name,  wsman_filter=None):
        '''Enumerate a resource.'''
        return common.enumerate_resource(self.client, resource_name, wsman_filter=wsman_filter, options=self.options)
