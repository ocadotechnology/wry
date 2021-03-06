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

'''
A simple class for accessing wsman style management interfaces like AMT

I'm afraid we just string-bash the XML into submission here.
'''


CONNECT_RETRIES = 3 # Number of times to retry a WSMan connection

CONNECT_DELAY = 0.25 # Number of seconds between retries


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
        'get': '',
        'enumerate': '',
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
        'enumerate': '',
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
    'CIM_Chassis' : {
        'enumerate': '',
    },
    'CIM_SystemBIOS' : {
        'get': '',
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

