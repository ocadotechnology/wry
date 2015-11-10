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

import re
import pywsman



def power_state_change(number):
    return '''^<\?xml version="1\.0"\?>
<s:Envelope xmlns:s="http://www\.w3\.org/2003/05/soap-envelope" xmlns:wsa="http://schemas\.xmlsoap\.org/ws/2004/08/addressing" xmlns:wsman="http://schemas\.dmtf\.org/wbem/wsman/1/wsman\.xsd" xmlns:n1="http://schemas\.dmtf\.org/wbem/wscim/1/cim-schema/2/CIM_PowerManagementService">
  <s:Header>
    <wsa:Action s:mustUnderstand="true">http://schemas\.dmtf\.org/wbem/wscim/1/cim-schema/2/CIM_PowerManagementService/RequestPowerStateChange</wsa:Action>
    <wsa:To s:mustUnderstand="true">http://fake_hostname:16992/wsman</wsa:To>
    <wsman:ResourceURI s:mustUnderstand="true">http://schemas\.dmtf\.org/wbem/wscim/1/cim-schema/2/CIM_PowerManagementService</wsman:ResourceURI>
    <wsa:MessageID s:mustUnderstand="true">uuid:[0-9a-f-]{36}</wsa:MessageID>
    <wsa:ReplyTo>
      <wsa:Address>http://schemas\.xmlsoap\.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
    </wsa:ReplyTo>
    <wsman:SelectorSet>
      <wsman:Selector Name="Name">Intel\(r\) AMT Power Management Service</wsman:Selector>
    </wsman:SelectorSet>
  </s:Header>
  <s:Body>
    <n1:RequestPowerStateChange_INPUT>
      <n1:PowerState>%s</n1:PowerState>
      <n1:ManagedElement>
        <wsa:Address>http://schemas\.xmlsoap\.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        <wsa:ReferenceParameters>
          <wsman:ResourceURI>http://schemas\.dmtf\.org/wbem/wscim/1/cim-schema/2/CIM_ComputerSystem</wsman:ResourceURI>
          <wsman:SelectorSet>
            <wsman:Selector Name="Name">ManagedSystem</wsman:Selector>
          </wsman:SelectorSet>
        </wsa:ReferenceParameters>
      </n1:ManagedElement>
    </n1:RequestPowerStateChange_INPUT>
  </s:Body>
</s:Envelope>$''' % number


def kvm_enable():
    return '''^<\?xml version="1\.0"\?>
<s:Envelope xmlns:s="http://www\.w3\.org/2003/05/soap-envelope" xmlns:wsa="http://schemas\.xmlsoap\.org/ws/2004/08/addressing" xmlns:wsman="http://schemas\.dmtf\.org/wbem/wsman/1/wsman\.xsd" xmlns:n1="http://schemas\.dmtf\.org/wbem/wscim/1/cim-schema/2/CIM_KVMRedirectionSAP">
  <s:Header>
    <wsa:Action s:mustUnderstand="true">http://schemas\.dmtf\.org/wbem/wscim/1/cim-schema/2/CIM_KVMRedirectionSAP/RequestStateChange</wsa:Action>
    <wsa:To s:mustUnderstand="true">http://fake_hostname:16992/wsman</wsa:To>
    <wsman:ResourceURI s:mustUnderstand="true">http://schemas\.dmtf\.org/wbem/wscim/1/cim-schema/2/CIM_KVMRedirectionSAP</wsman:ResourceURI>
    <wsa:MessageID s:mustUnderstand="true">uuid:[0-9a-f-]{36}</wsa:MessageID>
    <wsa:ReplyTo>
      <wsa:Address>http://schemas\.xmlsoap\.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
    </wsa:ReplyTo>
  </s:Header>
  <s:Body>
    <n1:RequestStateChange_INPUT>
      <n1:RequestedState>2</n1:RequestedState>
    </n1:RequestStateChange_INPUT>
  </s:Body>
</s:Envelope>$'''


set_boot_config_role = r'''^<\?xml version="1\.0"\?>
<s:Envelope xmlns:s="http://www\.w3\.org/2003/05/soap-envelope" xmlns:wsa="http://schemas\.xmlsoap\.org/ws/2004/08/addressing" xmlns:wsman="http://schemas\.dmtf\.org/wbem/wsman/1/wsman\.xsd">
  <s:Header>
    <wsa:Action s:mustUnderstand="true">http://schemas\.xmlsoap\.org/ws/2004/09/transfer/Get</wsa:Action>
    <wsa:To s:mustUnderstand="true">http://fake_hostname:16992/wsman</wsa:To>
    <wsman:ResourceURI s:mustUnderstand="true">http://schemas\.dmtf\.org/wbem/wscim/1/cim-schema/2/CIM_BootService</wsman:ResourceURI>
    <wsa:MessageID s:mustUnderstand="true">uuid:[0-9a-f-]{36}</wsa:MessageID>
    <wsa:ReplyTo>
      <wsa:Address>http://schemas\.xmlsoap\.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
    </wsa:ReplyTo>
  </s:Header>
  <s:Body/>
</s:Envelope>$'''


def set_boot_medium(medium):
    media = {
        'Network': ('Intel\(r\) AMT: Force PXE Boot', 'CIM:Network:1'),
        'Hard-Drive': ('Intel\(r\) AMT: Force Hard-drive Boot', 'CIM:Hard-Disk:1'),
        'CD/DVD': ('Intel\(r\) AMT: Force CD/DVD Boot', 'CIM:CD/DVD:1'),
    }
    return r'''^<\?xml version="1\.0"\?>
<s:Envelope xmlns:s="http://www\.w3\.org/2003/05/soap-envelope" xmlns:wsa="http://schemas\.xmlsoap\.org/ws/2004/08/addressing" xmlns:wsman="http://schemas\.dmtf\.org/wbem/wsman/1/wsman\.xsd" xmlns:n1="http://schemas\.dmtf\.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting">
  <s:Header>
    <wsa:Action s:mustUnderstand="true">http://schemas\.dmtf\.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting/ChangeBootOrder</wsa:Action>
    <wsa:To s:mustUnderstand="true">http://fake_hostname:16992/wsman</wsa:To>
    <wsman:ResourceURI s:mustUnderstand="true">http://schemas\.dmtf\.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting</wsman:ResourceURI>
    <wsa:MessageID s:mustUnderstand="true">uuid:[0-9a-f-]{36}</wsa:MessageID>
    <wsa:ReplyTo>
      <wsa:Address>http://schemas\.xmlsoap\.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
    </wsa:ReplyTo>
    <wsman:SelectorSet>
      <wsman:Selector Name="InstanceID">Intel\(r\) AMT: Boot Configuration 0</wsman:Selector>
    </wsman:SelectorSet>
  </s:Header>
  <s:Body>
    <n1:ChangeBootOrder_INPUT>
      <n1:Source>
        <wsa:Address>http://schemas\.xmlsoap\.org/ws/2004/08/addressing</wsa:Address>
        <wsa:ReferenceParameters>
          <wsman:ResourceURI>http://schemas\.dmtf\.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI>
          <wsman:SelectorSet>
            <wsman:Selector Name="InstanceID">%s</wsman:Selector>
          </wsman:SelectorSet>
        </wsa:ReferenceParameters>
      </n1:Source>
    </n1:ChangeBootOrder_INPUT>
  </s:Body>
</s:Envelope>$''' % media[medium][0]


def client_pull_factory():
    def client_pull(client, options, _, uri, context):
        if uri == 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting':
            if context == '25000000-0000-0000-0000-000000000000':
                return pywsman.create_doc_from_string(boot_source_setting_values.pop(0))
    boot_source_setting_values = [
        '''<?xml version="1.0" encoding="UTF-8"?>
<a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:h="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <a:Header>
    <b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To>
    <b:RelatesTo>uuid:4f89f08c-241b-141b-8004-80db73edaeb8</b:RelatesTo>
    <b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/PullResponse</b:Action>
    <b:MessageID>uuid:00000000-8086-8086-8086-00000000025E</b:MessageID>
    <c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</c:ResourceURI>
  </a:Header>
  <a:Body>
    <g:PullResponse>
      <g:EnumerationContext>25000000-0000-0000-0000-000000000000</g:EnumerationContext>
      <g:Items>
        <h:CIM_BootSourceSetting>
          <h:ElementName>Intel(r) AMT: Boot Source</h:ElementName>
          <h:FailThroughSupported>2</h:FailThroughSupported>
          <h:InstanceID>Intel(r) AMT: Force Hard-drive Boot</h:InstanceID>
          <h:StructuredBootString>CIM:Hard-Disk:1</h:StructuredBootString>
        </h:CIM_BootSourceSetting>
      </g:Items>
    </g:PullResponse>
  </a:Body>
</a:Envelope>''',
        '''<?xml version="1.0" encoding="UTF-8"?>
<a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:h="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <a:Header>
    <b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To>
    <b:RelatesTo>uuid:4f8a3a0d-241b-141b-8005-80db73edaeb8</b:RelatesTo>
    <b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/PullResponse</b:Action>
    <b:MessageID>uuid:00000000-8086-8086-8086-00000000025F</b:MessageID>
    <c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</c:ResourceURI>
  </a:Header>
  <a:Body>
    <g:PullResponse>
      <g:EnumerationContext>25000000-0000-0000-0000-000000000000</g:EnumerationContext>
      <g:Items>
        <h:CIM_BootSourceSetting>
          <h:ElementName>Intel(r) AMT: Boot Source</h:ElementName>
          <h:FailThroughSupported>2</h:FailThroughSupported>
          <h:InstanceID>Intel(r) AMT: Force PXE Boot</h:InstanceID>
          <h:StructuredBootString>CIM:Network:1</h:StructuredBootString>
        </h:CIM_BootSourceSetting>
      </g:Items>
    </g:PullResponse>
  </a:Body>
</a:Envelope>''',
        '''<?xml version="1.0" encoding="UTF-8"?>
<a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:h="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <a:Header>
    <b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To>
    <b:RelatesTo>uuid:4f8b3503-241b-141b-8006-80db73edaeb8</b:RelatesTo>
    <b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/PullResponse</b:Action>
    <b:MessageID>uuid:00000000-8086-8086-8086-000000000260</b:MessageID>
    <c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</c:ResourceURI>
  </a:Header>
  <a:Body>
    <g:PullResponse>
      <g:Items>
        <h:CIM_BootSourceSetting>
          <h:ElementName>Intel(r) AMT: Boot Source</h:ElementName>
          <h:FailThroughSupported>2</h:FailThroughSupported>
          <h:InstanceID>Intel(r) AMT: Force CD/DVD Boot</h:InstanceID>
          <h:StructuredBootString>CIM:CD/DVD:1</h:StructuredBootString>
        </h:CIM_BootSourceSetting>
      </g:Items>
      <g:EndOfSequence/>
    </g:PullResponse>
  </a:Body>
</a:Envelope>''']
    return client_pull


def client_enumerate(client, options, _, uri):
    if uri == 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting':
        return pywsman.create_doc_from_string('''<?xml version="1.0" encoding="UTF-8"?>
<a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <a:Header>
    <b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To>
    <b:RelatesTo>uuid:0041f82d-241a-141a-8002-80db73edaeb8</b:RelatesTo>
    <b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/EnumerateResponse</b:Action>
    <b:MessageID>uuid:00000000-8086-8086-8086-00000000021D</b:MessageID>
    <c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</c:ResourceURI>
  </a:Header>
  <a:Body>
    <g:EnumerateResponse>
      <g:EnumerationContext>25000000-0000-0000-0000-000000000000</g:EnumerationContext>
    </g:EnumerateResponse>
  </a:Body>
</a:Envelope>
''')
    else:
        raise RuntimeError


def client_get(*args, **kwargs):
    if args[-1] == 'http://intel.com/wbem/wscim/1/amt-schema/1/AMT_BootSettingData':
        return pywsman.create_doc_from_string('''<?xml version="1.0" encoding="UTF-8"?>
<a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://intel.com/wbem/wscim/1/amt-schema/1/AMT_BootSettingData" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <a:Header>
    <b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To>
    <b:RelatesTo>uuid:d6ae5d5e-2419-1419-8004-80db73edaeb8</b:RelatesTo>
    <b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/transfer/GetResponse</b:Action>
    <b:MessageID>uuid:00000000-8086-8086-8086-00000000011C</b:MessageID>
    <c:ResourceURI>http://intel.com/wbem/wscim/1/amt-schema/1/AMT_BootSettingData</c:ResourceURI>
  </a:Header>
  <a:Body>
    <g:AMT_BootSettingData>
      <g:BIOSPause>false</g:BIOSPause>
      <g:BIOSSetup>false</g:BIOSSetup>
      <g:BootMediaIndex>0</g:BootMediaIndex>
      <g:ConfigurationDataReset>false</g:ConfigurationDataReset>
      <g:ElementName>Intel(r) AMT Boot Configuration Settings</g:ElementName>
      <g:EnforceSecureBoot>false</g:EnforceSecureBoot>
      <g:FirmwareVerbosity>0</g:FirmwareVerbosity>
      <g:ForcedProgressEvents>false</g:ForcedProgressEvents>
      <g:IDERBootDevice>0</g:IDERBootDevice>
      <g:InstanceID>Intel(r) AMT:BootSettingData 0</g:InstanceID>
      <g:LockKeyboard>false</g:LockKeyboard>
      <g:LockPowerButton>false</g:LockPowerButton>
      <g:LockResetButton>false</g:LockResetButton>
      <g:LockSleepButton>false</g:LockSleepButton>
      <g:OwningEntity>Intel(r) AMT</g:OwningEntity>
      <g:ReflashBIOS>false</g:ReflashBIOS>
      <g:UseIDER>false</g:UseIDER>
      <g:UseSOL>false</g:UseSOL>
      <g:UseSafeMode>false</g:UseSafeMode>
      <g:UserPasswordBypass>false</g:UserPasswordBypass>
    </g:AMT_BootSettingData>
  </a:Body>
</a:Envelope>''')
    elif args[-1] == 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting':
        return pywsman.create_doc_from_string('''<?xml version="1.0" encoding="UTF-8"?>
<a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <a:Header>
    <b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To>
    <b:RelatesTo>uuid:6718d621-241c-141c-800e-80db73edaeb8</b:RelatesTo>
    <b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/transfer/GetResponse</b:Action>
    <b:MessageID>uuid:00000000-8086-8086-8086-000000000267</b:MessageID>
    <c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting</c:ResourceURI>
  </a:Header>
  <a:Body>
    <g:CIM_BootConfigSetting>
      <g:ElementName>Intel(r) AMT: Boot Configuration</g:ElementName>
      <g:InstanceID>Intel(r) AMT: Boot Configuration 0</g:InstanceID>
    </g:CIM_BootConfigSetting>
  </a:Body>
</a:Envelope>''')
    raise RuntimeError(args, kwargs)

