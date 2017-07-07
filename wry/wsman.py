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

import uuid
import requests
import xmltodict

'''
Created on 6 Jul 2017

A simple class for accessing wsman style management interfaces like AMT

I'm afraid we just string-bash the XML into submission here.

@author: adrian
'''


_NAMESPACES = {
    'soap':                 'http://www.w3.org/2003/05/soap-envelope',
    'addressing':           'http://schemas.xmlsoap.org/ws/2004/08/addressing',
    'addressing_anonymous': 'http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous',
    'wsman':                'http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd',
    'CIM':                  'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/',
    'IPS':                  'http://intel.com/wbem/wscim/1/ips-schema/1/',
    'AMT':                  'http://intel.com/wbem/wscim/1/amt-schema/1/',
}


RESOURCE_METHODS = {
    # Resource names can be added here, and their respective URIs should be
    # auto-generated.
    'CIM_AssociatedPowerManagementService': {
        'get': '',
    },
    'CIM_PowerManagementService': {
        'get': '',
        'request_power_state_change': '''
        <n1:RequestPowerStateChange_INPUT>
            <n1:PowerState>%%(power_state)d</n1:PowerState>
            <n1:ManagedElement>
                <wsa:Address>%(addressing_anonymous)s</wsa:Address>
                <wsa:ReferenceParameters>
                    <wsman:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ComputerSystem</wsman:ResourceURI>
                    <wsman:SelectorSet>
                        <wsman:Selector wsman:Name="Name">ManagedSystem</wsman:Selector>
                    </wsman:SelectorSet>
                </wsa:ReferenceParameters>
            </n1:ManagedElement>
        </n1:RequestPowerStateChange_INPUT>
''' % _NAMESPACES,
    },
    'CIM_ComputerSystem': {
        'get': ''
    },
    'CIM_BootConfigSetting': {
        'get': '',
        'change_boot_order': '''
''',
    },
    'CIM_BootSourceSetting': {
        'enumerate': '''
''',
        'pull': '''
''',
    },
    'CIM_BootService': {
        'get': '',
        'set_boot_config_role': '''
''',
    },
    'CIM_KVMRedirectionSAP': {
        'get': '',
        'put': '''
''',
    },
    'IPS_KVMRedirectionSettingData': {
        'get': '',
        'put': '''
''',
    },
    'IPS_OptInService': {
        'get': '',
        'enumerate': '''
''',
        'pull': '''
''',
        'put': '''
''',
    },
    'AMT_RedirectionService': {
        'get': '',
        'put': '''
''',
    },
    'AMT_TLSSettingData': {
        'get': '',
        'put': '''
''',
    },
    'AMT_BootCapabilities': {
        'get': '',
    },
    'AMT_BootSettingData': {
        'get': '',
        'put': '''
''',
    },
    'AMT_EthernetPortSettings': {
        'get': '',
        'put': '''
''',
    },
    'AMT_GeneralSettings': {
        'get': '',
        'put': '''
''',
    },
}


CONNECT_RETRIES = 3 # Number of times to retry a WSMan connection


RESOURCE_URIS = {name:_NAMESPACES[name.split('_')[0]] + name for name in RESOURCE_METHODS.keys()}
RESOURCE_URIS.update(_NAMESPACES)


ACTIONS_URIS = {
    'get':                  'http://schemas.xmlsoap.org/ws/2004/09/transfer/Get',
    'put':                  'http://schemas.xmlsoap.org/ws/2004/09/transfer/Put',
    'delete':               'http://schemas.xmlsoap.org/ws/2004/09/transfer/Delete',
    'create':               'http://schemas.xmlsoap.org/ws/2004/09/transfer/Create',
    'enumerate':            'http://schemas.xmlsoap.org/ws/2004/09/enumeration/Enumerate',
}


# Values that must be supplied when this template is used
#
# uri
# actionUri
# resourceUri
# setting (May be blank)
# uuid
# extraHeader
# body
#
WS_ENVELOPE = r'''<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="%(soap)s"
            xmlns:wsa="%(addressing)s"
            xmlns:wsman="%(wsman)s"
            xmlns:action="%%(resourceUri)s"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">%%(actionUri)s</wsa:Action>
        <wsa:To s:mustUnderstand="true">%%(uri)s</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">%%(resourceUri)s</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:%%(uuid)s</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
%%(extraHeader)s
    </s:Header>
    <s:Body>
%%(body)s
    </s:Body>
</s:Envelope>''' % _NAMESPACES


class wsmanResource(object):
    '''
    Class to represent a resource on a wsman compatible server
    '''

    def __init__(self, target = None, resource = None, username = None, password = None):
        '''
        Set up this resource

        @param target: the URL of the wsman service
        @param resource: the identifier of the resource containing the settings we are interested in
        '''
        self.target = target + "/wsman"
        self.resourceId = resource
        self.resourceUri = RESOURCE_URIS[self.resourceId]
        self.resource_methods = RESOURCE_METHODS[resource]
        self.username = username
        self.password = password

    def etree_to_dict(self, t):
        d = {t.tag : map(self.etree_to_dict, t.iterchildren())}
        d.update(('@' + k, v) for k, v in t.attrib.iteritems())
        d['text'] = t.text
        return d

#TODO Implement send/receive logic
    def request(self, params = {}):
        '''
        Send a request to the target and return the response

        '''
        params['uuid'] = uuid.uuid4()
        doc = WS_ENVELOPE % params
        print doc
        resp = requests.post(
            self.target,
            headers = {'content-type': 'application/soap+xml;charset=UTF-8'},
            auth = requests.auth.HTTPDigestAuth(self.username, self.password),
            data = doc,
            allow_redirects = False,
        )
        resp.raise_for_status()
        data = xmltodict.parse(resp.content)
        print resp.content
        print data
#        raise NotImplementedError("Need to be able to send stuff!!")

#TODO convert get to a request
    def get(self, setting = ''):
        '''
        Send a get request and return the result

        @param setting: the setting to get the value of (None for all in this resources)
        '''
        params = {
            'uri': self.target,
            'actionUri': ACTIONS_URIS['get'],
            'resourceUri': self.resourceUri,
            'setting': setting,
            'extraHeader': '',
            'body': self.resource_methods['get']
        }
        return self.request(params)

    def put(self, **kwargs):
        '''
        Get the current values, fill in new values and put back

        @param **kwargs: zero or more settings to put back to the wsman server
        '''
        pass

    def delete(self, **kwargs):
        '''
        Delete an instance
        '''
        raise NotImplementedError("Create/Delete not supported")

    def Create(self, **kwargs):
        '''
        Create an instance
        '''
        raise NotImplementedError("Create/Delete not supported")

    def enumerate(self):
        '''
        Return all instances of this Resource
        '''
        pass

    def invoke(self, method):
        '''
        Call a method and return the result

        @param method: the method name to call
        '''
        pass
