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



class WSManFault(Exception):
    def __init__(self, doc):
        self.doc = doc
        self.message = doc.fault().reason()
        self.detail = doc.fault().detail()
        self.subcode = doc.fault().subcode()
    def __str__(self):
        return self.message


class NonZeroReturn(Exception):
    pass


class AMTConnectFailure(Exception):
    pass


class XMLParseError(Exception):
    pass


class NoSupportedMethods(Exception):
    pass

