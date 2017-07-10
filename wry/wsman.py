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
import WryDict
from time import sleep

'''
Created on 6 Jul 2017

A simple class for accessing wsman style management interfaces like AMT

I'm afraid we just string-bash the XML into submission here.

@author: adrian
'''


CONNECT_RETRIES = 3 # Number of times to retry a WSMan connection


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
        'RequestPowerStateChange': '''
        <n1:RequestPowerStateChange_INPUT>
            <n1:PowerState>%%(power_state)d</n1:PowerState>
            <n1:ManagedElement>
                <wsa:Address>%(addressing_anonymous)s</wsa:Address>
                <wsa:ReferenceParameters>
                    <wsman:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ComputerSystem</wsman:ResourceURI>
                    <wsman:SelectorSet>
                        <wsman:Selector Name="Name">ManagedSystem</wsman:Selector>
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
        'ChangeBootOrder': '''
        <n1:ChangeBootOrder_INPUT>
            <n1:Source>
                <wsa:Address>%(addressing_anonymous)s</wsa:Address>
                <wsa:ReferenceParameters>
                    <wsman:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI>
                    <wsman:SelectorSet>
                        <wsman:Selector Name="InstanceID">%%(boot_device)s</wsman:Selector>
                    </wsman:SelectorSet>
                </wsa:ReferenceParameters>
            </n1:Source>
        </n1:ChangeBootOrder_INPUT>
''' % _NAMESPACES,
    },
    'CIM_BootSourceSetting': {
        'enumerate': '',
        'pull': '',
    },
    'CIM_BootService': {
        'get': '',
        'SetBootConfigRole': '''
        <n1:SetBootConfigRole_INPUT>
            <n1:BootConfigSetting>
                <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing</wsa:Address>
                <wsa:ReferenceParameters>
                     <wsman:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting</wsman:ResourceURI>
                     <wsman:SelectorSet>
                          <wsman:Selector Name="InstanceID">Intel(r) AMT: Boot Configuration 0</wsman:Selector>
                     </wsman:SelectorSet>
                </wsa:ReferenceParameters>
            </n1:BootConfigSetting>
            <n1:Role>%(role)s</n1:Role>
        </n1:SetBootConfigRole_INPUT>
''',
    },
    'CIM_KVMRedirectionSAP': {
        'get': '',
        'put': '',
        'RequestStateChange': '''
        <n1:RequestStateChange_INPUT>
            <n1:RequestedState>%(state)s</n1:RequestedState>
        </n1:RequestStateChange_INPUT>
''',
    },
    'IPS_KVMRedirectionSettingData': {
        'get': '',
        'put': '',
    },
    'IPS_OptInService': {
        'get': '',
        'enumerate': '',
        'pull': '',
        'put': '',
    },
    'AMT_RedirectionService': {
        'get': '',
        'put': '',
    },
    'AMT_TLSSettingData': {
        'get': '',
        'put': '',
    },
    'AMT_BootCapabilities': {
        'get': '',
    },
    'AMT_BootSettingData': {
        'get': '',
        'put': '',
    },
    'AMT_EthernetPortSettings': {
        'get': '',
        'put': '',
    },
    'AMT_GeneralSettings': {
        'get': '',
        'put': '',
    },
}


RESOURCE_URIS = {name:_NAMESPACES[name.split('_')[0]] + name for name in RESOURCE_METHODS.keys()}
RESOURCE_URIS.update(_NAMESPACES)


ACTIONS_URIS = {
    'get':                  'http://schemas.xmlsoap.org/ws/2004/09/transfer/Get',
    'put':                  'http://schemas.xmlsoap.org/ws/2004/09/transfer/Put',
    'delete':               'http://schemas.xmlsoap.org/ws/2004/09/transfer/Delete',
    'create':               'http://schemas.xmlsoap.org/ws/2004/09/transfer/Create',
    'enumerate':            'http://schemas.xmlsoap.org/ws/2004/09/enumeration/Enumerate',
    'pull':                 'http://schemas.xmlsoap.org/ws/2004/09/enumeration/Pull',
}


# Values that must be supplied when this template is used
#
# uri
# actionUri
# resourceUri
# uuid
# extraHeader
# body
#
WS_ENVELOPE = r'''<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="%(soap)s"
            xmlns:wsa="%(addressing)s"
            xmlns:wsman="%(wsman)s"
            xmlns:n1="%%(resourceUri)s"
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

WS_ENUM_ENVELOPE = r'''<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="%(soap)s"
            xmlns:wsa="%(addressing)s"
            xmlns:wsman="%(wsman)s"
            xmlns:wsen="http://schemas.xmlsoap.org/ws/2004/09/enumeration"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">%%(actionUri)s</wsa:Action>
        <wsa:To s:mustUnderstand="true">%%(uri)s</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">%%(resourceUri)s</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:%%(uuid)s</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
    </s:Header>
    <s:Body>
        <wsen:Enumerate/>
    </s:Body>
</s:Envelope>''' % _NAMESPACES

WS_PULL_ENVELOPE = r'''<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="%(soap)s"
            xmlns:wsa="%(addressing)s"
            xmlns:wsman="%(wsman)s"
            xmlns:wsen="http://schemas.xmlsoap.org/ws/2004/09/enumeration"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">%%(actionUri)s</wsa:Action>
        <wsa:To s:mustUnderstand="true">%%(uri)s</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">%%(resourceUri)s</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:%%(uuid)s</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
    </s:Header>
    <s:Body>
        <wsen:Pull>
            <wsen:EnumerationContext>%%(enumctx)s</wsen:EnumerationContext>
        </wsen:Pull>
    </s:Body>
</s:Envelope>''' % _NAMESPACES

AMT_PROTOCOL_PORT_MAP = {
    'http': 16992,
    'https': 16993,
}

class wsmanResource(object):
    '''
    Class to represent a resource on a wsman compatible server
    '''

    def __init__(self, target = None, is_ssl = False, username = None, password = None, resource = None):
        '''
        Set up this resource

        @param target: the hostname or IP address of the wsman service
        @param is_ssl: should we communicate using SSL?
        @param resource: the identifier of the resource containing the settings we are interested in
        @param username: the username to log in with
        @param password: the password to log in with
        '''
        if is_ssl:
            scheme = 'https'
        else:
            scheme = 'http'
        port = AMT_PROTOCOL_PORT_MAP[scheme]
        self.target = scheme + "://" + target + ":" + str(port) + "/wsman"
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

    def request(self, doc = None, params = {}):
        '''
        Send a request to the target and return the response

        '''
        params['uuid'] = uuid.uuid4()
        if enumerate:
            doc = doc % params
        else:
            doc = doc % params
        for _ in range(CONNECT_RETRIES + 1):
            try:
                resp = requests.post(
                    self.target,
                    timeout = (2, 1),
                    headers = {'content-type': 'application/soap+xml;charset=UTF-8'},
                    auth = requests.auth.HTTPDigestAuth(self.username, self.password),
                    data = doc,
                    allow_redirects = False,
                )
                resp.raise_for_status()
                return WryDict.WryDict.from_xml(resp.content)
            except requests.exceptions.ConnectTimeout:
                print("Failed, retrying")
                sleep(.1)
            except:
                raise

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
        response = self.request(doc = WS_ENVELOPE, params = params)
        if len(setting) > 0:
            response = response[self.resourceId][setting]
        return response

    def put(self, **kwargs):
        '''
        Get the current values, fill in new values and put back

        @param **kwargs: zero or more settings to put back to the wsman server
        '''
        current = self.get()
        for k, v in kwargs.iteritems():
            current[self.resourceId][k] = v
        params = {
            'uri': self.target,
            'actionUri': ACTIONS_URIS['put'],
            'resourceUri': self.resourceUri,
            'setting': '',
            'extraHeader': '',
            'body': current.to_xml
        }
        return self.request(doc = WS_ENVELOPE, params = params)

#    def delete(self, **kwargs):
#        '''
#        Delete an instance
#        '''
#        params = {
#            'uri': self.target,
#            'actionUri': ACTIONS_URIS['delete'],
#            'resourceUri': self.resourceUri,
#            'setting': '',
#            'extraHeader': '',
#            'body': self.resource_methods['delete'] % kwargs
#        }
#        return self.request(doc = WS_ENVELOPE, params = params)
#
#    def Create(self, **kwargs):
#        '''
#        Create an instance
#        '''
#        params = {
#            'uri': self.target,
#            'actionUri': ACTIONS_URIS['create'],
#            'resourceUri': self.resourceUri,
#            'setting': '',
#            'extraHeader': '',
#            'body': self.resource_methods['create'] % kwargs
#        }
#        return self.request(doc = WS_ENVELOPE, params = params)

    def enumerate(self, **kwargs):
        '''
        Return all instances of this Resource
        '''
        params = {
            'uri': self.target,
            'actionUri': ACTIONS_URIS['enumerate'],
            'resourceUri': self.resourceUri,
            'setting': '',
            'extraHeader': '',
            'body': self.resource_methods['enumerate'] % kwargs
        }
        enum_response = self.request(doc = WS_ENUM_ENVELOPE, params = params)
        params['enumctx'] = enum_response['EnumerateResponse']['EnumerationContext']
        params['actionUri'] = ACTIONS_URIS['pull']
        output = WryDict.WryDict({self.resourceId:[]})
        while params['enumctx']:
            data = self.request(doc = WS_PULL_ENVELOPE, params = params)
            if not data['PullResponse'].has_key('EnumerationContext'):
                params['enumctx'] = None
            output[self.resourceId].append(data['PullResponse']['Items'][self.resourceId])
        return output

    def invoke(self, method, **kwargs):
        '''
        Call a method and return the result

        @param method: the method name to call
        '''
        if not self.resource_methods.has_key(method):
            raise Exception("Method '%s' not defined" % method)
        extraHeader = ''
        if kwargs.has_key('headerSelectior') and kwargs.has_key('headerSelectorType'):
            '<wsman:SelectorSet><wsman:Selector Name="%(headerSelectorType)s">%(headerSelector)s</wsman:Selector></wsman:SelectorSet>' % kwargs
        params = {
            'uri': self.target,
            'actionUri': self.resourceUri + "/" + method,
            'resourceUri': self.resourceUri,
            'setting': '',
            'extraHeader': extraHeader,
            'body': self.resource_methods[method] % kwargs
        }
        return self.request(doc = WS_ENVELOPE, params = params)


class wsmanModule(object):
    '''
    Base class for all wry modules
    '''
    RESOURCES = {
    }

    def __init__(self, device):
        '''
        Create resources for each defined resource
        '''
        for k in self.RESOURCES.keys():
            self.RESOURCES[k] = wsmanResource(
                target = device.target,
                is_ssl = device.is_ssl,
                username = device.username,
                password = device.password,
                resource = self.RESOURCES[k]
            )


