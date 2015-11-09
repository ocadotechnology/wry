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

import unittest
import mock
import pywsman
import tempfile
import os
import wry
from wry.tests import data


class WryTest(unittest.TestCase):
    '''Tests for device power management/control.'''

    def setUp(self):
        super(WryTest, self).setUp()
        self.options = pywsman.ClientOptions()
        self.client = pywsman.Client('fake_hostname', 16992, '/wsman', 'http', 'user', 'password')
        fd, self.dumpfile_name = tempfile.mkstemp()
        self.dumpfile = pywsman.fopen(self.dumpfile_name, 'w')
        self.client.set_dumpfile(self.dumpfile)
        self.options.set_dump_request()

    def tearDown(self):
        pywsman.fclose(self.dumpfile)
        os.remove(self.dumpfile_name)
        super(WryTest, self).tearDown()


class PowerTests(WryTest):
    '''Tests for device power management/control.'''

    def setUp(self):
        super(PowerTests, self).setUp()
        self.power = wry.device.AMTPower(self.client, self.options)

    @mock.patch('wry.decorators.CONNECT_RETRIES', 0)
    def test_power_on(self):
        try:
            self.power.turn_on()
        except wry.exceptions.AMTConnectFailure:
            pass
        with open(self.dumpfile_name, 'r') as output:
            self.assertRegexpMatches(
                output.read(),
                data.power_state_change(2),
            )


class KVMTests(WryTest):
    '''Tests for device power management/control.'''

    def setUp(self):
        super(KVMTests, self).setUp()
        self.kvm = wry.device.AMTKVM(self.client, self.options)

    @mock.patch('wry.decorators.CONNECT_RETRIES', 0)
    def test_kvm_enable(self):
        try:
            self.kvm.enabled = True
        except wry.exceptions.AMTConnectFailure:
            pass
        with open(self.dumpfile_name, 'r') as output:
            self.assertRegexpMatches(
                output.read(),
                data.kvm_enable(),
            )


class BootTests(WryTest):
    '''Tests for device power management/control.'''

    def setUp(self):
        super(BootTests, self).setUp()
        self.boot = wry.device.AMTBoot(self.client, self.options)

    @mock.patch.multiple(pywsman.Client,
        get=data.client_get,
        enumerate=data.client_enumerate,
        pull=data.client_pull_factory(),
    )
    @mock.patch('wry.decorators.CONNECT_RETRIES', 0)
    def test_set_hdd_boot(self):
        try:
            self.boot.medium = 'Hard-Disk'
        except wry.exceptions.AMTConnectFailure:
            pass
        with open(self.dumpfile_name, 'r') as output:
            self.assertRegexpMatches(
                output.read(),
                data.set_boot_medium('Hard-Drive'),
            )

    @mock.patch.multiple(pywsman.Client,
        get=data.client_get,
        enumerate=data.client_enumerate,
        pull=data.client_pull_factory(),
    )
    @mock.patch('wry.decorators.CONNECT_RETRIES', 0)
    def test_set_cd_boot(self):
        try:
            self.boot.medium = 'CD/DVD'
        except wry.exceptions.AMTConnectFailure:
            pass
        with open(self.dumpfile_name, 'r') as output:
            self.assertRegexpMatches(
                output.read(),
                data.set_boot_medium('CD/DVD'),
            )

    @mock.patch.multiple(pywsman.Client,
        get=data.client_get,
        enumerate=data.client_enumerate,
        pull=data.client_pull_factory(),
    )
    @mock.patch('wry.decorators.CONNECT_RETRIES', 0)
    def test_set_pxe_boot(self):
        try:
            self.boot.medium = 'Network'
        except wry.exceptions.AMTConnectFailure:
            pass
        with open(self.dumpfile_name, 'r') as output:
            self.assertRegexpMatches(
                output.read(),
                data.set_boot_medium('Network'),
            )

    @mock.patch('wry.decorators.CONNECT_RETRIES', 0)
    def test_set_boot_config_role(self):
        try:
            self.boot._set_boot_config_role()
        except wry.exceptions.AMTConnectFailure:
            pass
        with open(self.dumpfile_name, 'r') as output:
            self.assertRegexpMatches(
                output.read(),
                data.set_boot_config_role,
            )

if __name__ == '__main__':
    unittest.main()
