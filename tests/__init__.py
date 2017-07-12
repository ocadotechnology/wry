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
import os.path

'''
Created on 12 Jul 2017

@author: adrian
'''

if __name__ == '__main__':
    print "Running"
    suite = unittest.TestLoader().discover(
        start_dir = os.path.dirname(os.path.abspath(__file__)),
        pattern = "test_*.py",
        top_level_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    unittest.TextTestRunner().run(suite)
