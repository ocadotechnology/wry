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


CONNECT_RETRIES = 3 # Number of times to retry a WSMan connection


_URI_PREFIXES = {
    'CIM': 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/',
    'IPS': 'http://intel.com/wbem/wscim/1/ips-schema/1/',
    'AMT': 'http://intel.com/wbem/wscim/1/amt-schema/1/',
}


RESOURCE_METHODS = {
        # Resource names can be added here, and their respective URIs should be
        # auto-generated.
        'CIM_AssociatedPowerManagementService': ['get'],
        'CIM_PowerManagementService': ['get', 'request_power_state_change'],
        'CIM_ComputerSystem': ['get'],
        'CIM_BootConfigSetting': ['get', 'change_boot_order'],
        'CIM_BootSourceSetting': ['enumerate', 'pull'],
        'CIM_BootService': ['get', 'set_boot_config_role'],
        'CIM_KVMRedirectionSAP': ['get', 'put'],
        'IPS_KVMRedirectionSettingData': ['get', 'put'],
        'AMT_RedirectionService': ['get', 'put'],
        'AMT_TLSSettingData': ['get', 'put'],
        'AMT_BootCapabilities': ['get'],
        'AMT_BootSettingData': ['get', 'put'],
        'AMT_EthernetPortSettings': ['get', 'put'],
        'AMT_GeneralSettings': ['get', 'put'],
}


RESOURCE_URIs = {}
for name in RESOURCE_METHODS.keys():
    prefix = name.split('_')[0]
    RESOURCE_URIs[name] = _URI_PREFIXES[prefix] + name


SCHEMAS = dict(
    addressing = 'http://schemas.xmlsoap.org/ws/2004/08/addressing',
    addressing_anonymous = 'http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous',
    wsman = 'http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd',
)
