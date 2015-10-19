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

#: Do not retry connections, as there is nothing to connect to. This does not work :(
mock.patch('wry.decorators.retry', lambda x: x).start()
from wry.tests import data


class PowerTests(unittest.TestCase):
    '''Tests for device power management/control.'''

    def setUp(self):
        options = pywsman.ClientOptions()
        client = pywsman.Client('fake_hostname', 16992, '/wsman', 'http', 'user', 'password')
        fd, self.dumpfile_name = tempfile.mkstemp()
        self.dumpfile = pywsman.fopen(self.dumpfile_name, 'w')
        client.set_dumpfile(self.dumpfile)
        options.set_dump_request()
        self.power = wry.device.AMTPower(client, options)

    def tearDown(self):
        pywsman.fclose(self.dumpfile)
        os.remove(self.dumpfile_name)

    def test_power_on(self):
        try:
            self.power.turn_on()
        except wry.exceptions.AMTConnectFailure:
            pass
        with open(self.dumpfile_name, 'r') as output:
            self.assertTrue(
                data.power_state_change(2).match(
                    output.read()
                )
            )


if __name__ == '__main__':
    unittest.main()
