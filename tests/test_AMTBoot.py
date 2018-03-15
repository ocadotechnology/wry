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

import TestBase
import wry

class Test(TestBase.TestBase):
    def setUp(self):
        TestBase.TestBase.setUp(self)
        self.boot = wry.AMTBoot(self.DEVICE)

    def tearDown(self):
        TestBase.TestBase.tearDown(self)

# This not only tests the supportedMedia method but also the enumerate workflow
    def testSupportedMedia(self):
        'Supported media'
        self.expectXML = [
            """<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"
            xmlns:wsen="http://schemas.xmlsoap.org/ws/2004/09/enumeration"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/Enumerate</wsa:Action>
        <wsa:To s:mustUnderstand="true">http://:16992/wsman</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
    </s:Header>
    <s:Body>
        <wsen:Enumerate/>
    </s:Body>
</s:Envelope>""",
            """<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"
            xmlns:wsen="http://schemas.xmlsoap.org/ws/2004/09/enumeration"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/Pull</wsa:Action>
        <wsa:To s:mustUnderstand="true">http://:16992/wsman</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
    </s:Header>
    <s:Body>
        <wsen:Pull>
            <wsen:EnumerationContext>01000000-0000-0000-0000-000000000000</wsen:EnumerationContext>
        </wsen:Pull>
    </s:Body>
</s:Envelope>""",
            """<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"
            xmlns:wsen="http://schemas.xmlsoap.org/ws/2004/09/enumeration"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/Pull</wsa:Action>
        <wsa:To s:mustUnderstand="true">http://:16992/wsman</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
    </s:Header>
    <s:Body>
        <wsen:Pull>
            <wsen:EnumerationContext>01000000-0000-0000-0000-000000000000</wsen:EnumerationContext>
        </wsen:Pull>
    </s:Body>
</s:Envelope>""",
            """<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"
            xmlns:wsen="http://schemas.xmlsoap.org/ws/2004/09/enumeration"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/Pull</wsa:Action>
        <wsa:To s:mustUnderstand="true">http://:16992/wsman</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
    </s:Header>
    <s:Body>
        <wsen:Pull>
            <wsen:EnumerationContext>01000000-0000-0000-0000-000000000000</wsen:EnumerationContext>
        </wsen:Pull>
    </s:Body>
</s:Envelope>""",
        ]
        self.respondXML = [
            """<?xml version="1.0" encoding="UTF-8"?><a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><a:Header><b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To><b:RelatesTo>uuid:879cf1c3-a3fe-4439-abb5-d3ea8aecff90</b:RelatesTo><b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/EnumerateResponse</b:Action><b:MessageID>uuid:00000000-8086-8086-8086-000000000001</b:MessageID><c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</c:ResourceURI></a:Header><a:Body><g:EnumerateResponse><g:EnumerationContext>01000000-0000-0000-0000-000000000000</g:EnumerationContext></g:EnumerateResponse></a:Body></a:Envelope>""",
            """<?xml version="1.0" encoding="UTF-8"?><a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:h="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><a:Header><b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To><b:RelatesTo>uuid:03071916-01cd-4227-be2f-2bb0d3f843d0</b:RelatesTo><b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/PullResponse</b:Action><b:MessageID>uuid:00000000-8086-8086-8086-000000000002</b:MessageID><c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</c:ResourceURI></a:Header><a:Body><g:PullResponse><g:EnumerationContext>01000000-0000-0000-0000-000000000000</g:EnumerationContext><g:Items><h:CIM_BootSourceSetting><h:ElementName>Intel(r) AMT: Boot Source</h:ElementName><h:FailThroughSupported>2</h:FailThroughSupported><h:InstanceID>Intel(r) AMT: Force Hard-drive Boot</h:InstanceID><h:StructuredBootString>CIM:Hard-Disk:1</h:StructuredBootString></h:CIM_BootSourceSetting></g:Items></g:PullResponse></a:Body></a:Envelope>""",
            """<?xml version="1.0" encoding="UTF-8"?><a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:h="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><a:Header><b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To><b:RelatesTo>uuid:32f056ea-5739-4b02-ac91-bf654a89289b</b:RelatesTo><b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/PullResponse</b:Action><b:MessageID>uuid:00000000-8086-8086-8086-000000000003</b:MessageID><c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</c:ResourceURI></a:Header><a:Body><g:PullResponse><g:EnumerationContext>01000000-0000-0000-0000-000000000000</g:EnumerationContext><g:Items><h:CIM_BootSourceSetting><h:ElementName>Intel(r) AMT: Boot Source</h:ElementName><h:FailThroughSupported>2</h:FailThroughSupported><h:InstanceID>Intel(r) AMT: Force PXE Boot</h:InstanceID><h:StructuredBootString>CIM:Network:1</h:StructuredBootString></h:CIM_BootSourceSetting></g:Items></g:PullResponse></a:Body></a:Envelope>""",
            """<?xml version="1.0" encoding="UTF-8"?><a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:h="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><a:Header><b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To><b:RelatesTo>uuid:246adfb8-52cf-4843-819f-d7594c6185e1</b:RelatesTo><b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/PullResponse</b:Action><b:MessageID>uuid:00000000-8086-8086-8086-000000000004</b:MessageID><c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</c:ResourceURI></a:Header><a:Body><g:PullResponse><g:Items><h:CIM_BootSourceSetting><h:ElementName>Intel(r) AMT: Boot Source</h:ElementName><h:FailThroughSupported>2</h:FailThroughSupported><h:InstanceID>Intel(r) AMT: Force CD/DVD Boot</h:InstanceID><h:StructuredBootString>CIM:CD/DVD:1</h:StructuredBootString></h:CIM_BootSourceSetting></g:Items><g:EndOfSequence></g:EndOfSequence></g:PullResponse></a:Body></a:Envelope>""",
        ]
        response = self.boot.supported_media
        self.assertIn("Hard-Disk", response)
        self.assertIn("Network", response)
        self.assertIn("CD/DVD", response)

    def testSetMedium(self):
        'Setting the next boot device'
        self.expectXML = [
            """<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"
            xmlns:wsen="http://schemas.xmlsoap.org/ws/2004/09/enumeration"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/Enumerate</wsa:Action>
        <wsa:To s:mustUnderstand="true">http://:16992/wsman</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
    </s:Header>
    <s:Body>
        <wsen:Enumerate/>
    </s:Body>
</s:Envelope>""",
"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"
            xmlns:wsen="http://schemas.xmlsoap.org/ws/2004/09/enumeration"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/Pull</wsa:Action>
        <wsa:To s:mustUnderstand="true">http://:16992/wsman</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
    </s:Header>
    <s:Body>
        <wsen:Pull>
            <wsen:EnumerationContext>01000000-0000-0000-0000-000000000000</wsen:EnumerationContext>
        </wsen:Pull>
    </s:Body>
</s:Envelope>""",
"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"
            xmlns:wsen="http://schemas.xmlsoap.org/ws/2004/09/enumeration"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/Pull</wsa:Action>
        <wsa:To s:mustUnderstand="true">http://:16992/wsman</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
    </s:Header>
    <s:Body>
        <wsen:Pull>
            <wsen:EnumerationContext>01000000-0000-0000-0000-000000000000</wsen:EnumerationContext>
        </wsen:Pull>
    </s:Body>
</s:Envelope>""",
"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"
            xmlns:wsen="http://schemas.xmlsoap.org/ws/2004/09/enumeration"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/Pull</wsa:Action>
        <wsa:To s:mustUnderstand="true">http://:16992/wsman</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
    </s:Header>
    <s:Body>
        <wsen:Pull>
            <wsen:EnumerationContext>01000000-0000-0000-0000-000000000000</wsen:EnumerationContext>
        </wsen:Pull>
    </s:Body>
</s:Envelope>""",
"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"
            xmlns:n1="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/transfer/Get</wsa:Action>
        <wsa:To s:mustUnderstand="true">http://:16992/wsman</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>

    </s:Header>
    <s:Body>

    </s:Body>
</s:Envelope>""",
"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"
            xmlns:n1="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting/ChangeBootOrder</wsa:Action>
        <wsa:To s:mustUnderstand="true">http://:16992/wsman</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
<wsman:SelectorSet><wsman:Selector Name="InstanceID">Intel(r) AMT: Boot Configuration 0</wsman:Selector></wsman:SelectorSet>
    </s:Header>
    <s:Body>

        <n1:ChangeBootOrder_INPUT>
            <n1:Source>
                <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
                <wsa:ReferenceParameters>
                    <wsman:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI>
                    <wsman:SelectorSet>
                        <wsman:Selector Name="InstanceID">Intel(r) AMT: Force PXE Boot</wsman:Selector>
                    </wsman:SelectorSet>
                </wsa:ReferenceParameters>
            </n1:Source>
        </n1:ChangeBootOrder_INPUT>

    </s:Body>
</s:Envelope>""",
"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"
            xmlns:n1="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootService"
            >
    <s:Header>
        <wsa:Action s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootService/SetBootConfigRole</wsa:Action>
        <wsa:To s:mustUnderstand="true">http://:16992/wsman</wsa:To>
        <wsman:ResourceURI s:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootService</wsman:ResourceURI>
        <wsa:MessageID s:mustUnderstand="true">uuid:</wsa:MessageID>
        <wsa:ReplyTo>
            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address>
        </wsa:ReplyTo>
<wsman:SelectorSet><wsman:Selector Name="Name">Intel(r) AMT Boot Service</wsman:Selector></wsman:SelectorSet>
    </s:Header>
    <s:Body>

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
            <n1:Role>1</n1:Role>
        </n1:SetBootConfigRole_INPUT>

    </s:Body>
</s:Envelope>""",
        ]
        self.respondXML = [
"""<?xml version="1.0" encoding="UTF-8"?><a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><a:Header><b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To><b:RelatesTo>uuid:f77dcaf5-ef68-460b-9963-e5526f64ce82</b:RelatesTo><b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/EnumerateResponse</b:Action><b:MessageID>uuid:00000000-8086-8086-8086-000000000001</b:MessageID><c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</c:ResourceURI></a:Header><a:Body><g:EnumerateResponse><g:EnumerationContext>01000000-0000-0000-0000-000000000000</g:EnumerationContext></g:EnumerateResponse></a:Body></a:Envelope>""",
"""<?xml version="1.0" encoding="UTF-8"?><a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:h="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><a:Header><b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To><b:RelatesTo>uuid:33e6476d-0a7b-4512-8668-30f1443b6814</b:RelatesTo><b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/PullResponse</b:Action><b:MessageID>uuid:00000000-8086-8086-8086-000000000002</b:MessageID><c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</c:ResourceURI></a:Header><a:Body><g:PullResponse><g:EnumerationContext>01000000-0000-0000-0000-000000000000</g:EnumerationContext><g:Items><h:CIM_BootSourceSetting><h:ElementName>Intel(r) AMT: Boot Source</h:ElementName><h:FailThroughSupported>2</h:FailThroughSupported><h:InstanceID>Intel(r) AMT: Force Hard-drive Boot</h:InstanceID><h:StructuredBootString>CIM:Hard-Disk:1</h:StructuredBootString></h:CIM_BootSourceSetting></g:Items></g:PullResponse></a:Body></a:Envelope>""",
"""<?xml version="1.0" encoding="UTF-8"?><a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:h="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><a:Header><b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To><b:RelatesTo>uuid:7be5d16b-1282-4c5e-8f72-056d0fc391da</b:RelatesTo><b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/PullResponse</b:Action><b:MessageID>uuid:00000000-8086-8086-8086-000000000003</b:MessageID><c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</c:ResourceURI></a:Header><a:Body><g:PullResponse><g:EnumerationContext>01000000-0000-0000-0000-000000000000</g:EnumerationContext><g:Items><h:CIM_BootSourceSetting><h:ElementName>Intel(r) AMT: Boot Source</h:ElementName><h:FailThroughSupported>2</h:FailThroughSupported><h:InstanceID>Intel(r) AMT: Force PXE Boot</h:InstanceID><h:StructuredBootString>CIM:Network:1</h:StructuredBootString></h:CIM_BootSourceSetting></g:Items></g:PullResponse></a:Body></a:Envelope>""",
"""<?xml version="1.0" encoding="UTF-8"?><a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:h="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><a:Header><b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To><b:RelatesTo>uuid:eaae8df1-5934-4ff5-a70f-61a2c95daef5</b:RelatesTo><b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/enumeration/PullResponse</b:Action><b:MessageID>uuid:00000000-8086-8086-8086-000000000004</b:MessageID><c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</c:ResourceURI></a:Header><a:Body><g:PullResponse><g:Items><h:CIM_BootSourceSetting><h:ElementName>Intel(r) AMT: Boot Source</h:ElementName><h:FailThroughSupported>2</h:FailThroughSupported><h:InstanceID>Intel(r) AMT: Force CD/DVD Boot</h:InstanceID><h:StructuredBootString>CIM:CD/DVD:1</h:StructuredBootString></h:CIM_BootSourceSetting></g:Items><g:EndOfSequence></g:EndOfSequence></g:PullResponse></a:Body></a:Envelope>""",
"""<?xml version="1.0" encoding="UTF-8"?><a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><a:Header><b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To><b:RelatesTo>uuid:09c9672a-4bb0-48ed-a071-00405002803b</b:RelatesTo><b:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/transfer/GetResponse</b:Action><b:MessageID>uuid:00000000-8086-8086-8086-000000000005</b:MessageID><c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting</c:ResourceURI></a:Header><a:Body><g:CIM_BootConfigSetting><g:ElementName>Intel(r) AMT: Boot Configuration</g:ElementName><g:InstanceID>Intel(r) AMT: Boot Configuration 0</g:InstanceID></g:CIM_BootConfigSetting></a:Body></a:Envelope>""",
"""<?xml version="1.0" encoding="UTF-8"?><a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><a:Header><b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To><b:RelatesTo>uuid:52a41ed8-55fa-418b-8f84-bdd3a6b7e736</b:RelatesTo><b:Action a:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting/ChangeBootOrderResponse</b:Action><b:MessageID>uuid:00000000-8086-8086-8086-000000000006</b:MessageID><c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting</c:ResourceURI></a:Header><a:Body><g:ChangeBootOrder_OUTPUT><g:ReturnValue>0</g:ReturnValue></g:ChangeBootOrder_OUTPUT></a:Body></a:Envelope>""",
"""<?xml version="1.0" encoding="UTF-8"?><a:Envelope xmlns:a="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:c="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:d="http://schemas.xmlsoap.org/ws/2005/02/trust" xmlns:e="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:f="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:g="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootService" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><a:Header><b:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</b:To><b:RelatesTo>uuid:7594f06b-cebd-474a-b989-652c018d26cc</b:RelatesTo><b:Action a:mustUnderstand="true">http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootService/SetBootConfigRoleResponse</b:Action><b:MessageID>uuid:00000000-8086-8086-8086-000000000007</b:MessageID><c:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootService</c:ResourceURI></a:Header><a:Body><g:SetBootConfigRole_OUTPUT><g:ReturnValue>0</g:ReturnValue></g:SetBootConfigRole_OUTPUT></a:Body></a:Envelope>""",
        ]
        self.boot.medium = "Network"
