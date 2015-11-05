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
