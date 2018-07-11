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

import unittest
import sys
import os.path
import re
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent)
import requests

class DEVICE:
    '''
    Simple class to provide the data normally provided by AMTDevice
    '''
    target = ""
    is_ssl = False
    username = None
    password = None
    debug = True
    showxml = False


class RESPONSE:
    def __init__(self, content):
        self.content = content

    def raise_for_status(self):
        pass

class TestBase(unittest.TestCase):
    '''
    Base class of all unittests.

    Among other things this overrides methods in the requests class to allow unittesting
    '''

    UUID = re.compile("uuid:.{36}")
    PRINT_DATA = False # Print the conversation to enable debugging failing tests

    def setUp(self):
        '''
        Constructor
        '''
        self.DEVICE = DEVICE
        requests.post = self._requests_post

    def tearDown(self):
        pass

    def _requests_post(self, url, data = None, json = None, **kwargs):
        '''
        Check request and send response as though it was a network connection
        '''
        req = self.expectXML.pop(0)
        if self.PRINT_DATA:
            print(len(data))
        data = self.UUID.sub("uuid:", data)
        if self.PRINT_DATA or (data != req):
            print(len(data), "\n", data, "\n=========\n", len(req), "\n", req , "\n==========\n", data==req, "\n")
        self.assertEqual(data, req, "Request does not match")
        resp = self.respondXML.pop(0)
        return RESPONSE(resp)
