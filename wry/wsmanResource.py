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

from . import wsmanData
import uuid
import requests
from . import WryDict
from time import sleep


class wsmanResource(object):
    '''
    Class to represent a resource on a wsman compatible server
    '''

    def __init__(self, target = None, is_ssl = False, username = None, password = None, resource = None, debug = False, showxml = False):
        '''
        Set up this resource

        @param target: the hostname or IP address of the wsman service
        @param is_ssl: should we communicate using SSL?
        @param resource: the identifier of the resource containing the settings we are interested in
        @param username: the username to log in with
        @param password: the password to log in with
        @param debug: enable debugging output
        @param showxml: enable output of XML transactions
        '''
        if is_ssl:
            scheme = 'https'
        else:
            scheme = 'http'
        port = wsmanData.AMT_PROTOCOL_PORT_MAP[scheme]
        self.target = scheme + "://" + target + ":" + str(port) + "/wsman"
        self.resourceId = resource
        self.resourceUri = wsmanData.RESOURCE_URIS[self.resourceId]
        self.resource_methods = wsmanData.RESOURCE_METHODS[resource]
        self.username = username
        self.password = password
        self.debug = debug
        self.showxml = showxml

    def etree_to_dict(self, t):
        d = {t.tag : map(self.etree_to_dict, t.iterchildren())}
        d.update(('@' + k, v) for k, v in t.attrib.iteritems())
        d['text'] = t.text
        return d

    def request(self, doc = None, params = {}):
        '''
        Send a request to the target and return the response

        '''
        params['uuid'] = uuid.uuid4()
        if enumerate:
            doc = doc % params
        else:
            doc = doc % params
        if self.showxml:
            print("===== Request =====")
            print(doc)
            print("===================")
        for _ in range(wsmanData.CONNECT_RETRIES + 1):
            try:
                if self.debug:
                    print("Connecting to %s" % (self.target,))
                resp = requests.post(
                    self.target,
                    timeout = (0.1, 5),
                    headers = {'content-type': 'application/soap+xml;charset=UTF-8'},
                    auth = requests.auth.HTTPDigestAuth(self.username, self.password),
                    data = doc,
                    allow_redirects = False,
                )
                if self.showxml:
                    print("===== Response =====")
                    print(resp.content)
                    print("====================")
                resp.raise_for_status()
                return WryDict.WryDict.from_xml(resp.content)
            except:
                raise
                if self.debug:
                    print("Failed, retrying")
                sleep(wsmanData.CONNECT_DELAY)

    def get(self, setting = '', **kwargs):
        '''
        Send a get request and return the result

        @param setting: the setting to get the value of (None for all in this resources)
        '''
        extraHeader = ''
        if 'headerSelector' in kwargs and 'headerSelectorType' in kwargs:
            extraHeader = '<wsman:SelectorSet><wsman:Selector Name="%(headerSelectorType)s">%(headerSelector)s</wsman:Selector></wsman:SelectorSet>' % kwargs
        params = {
            'uri': self.target,
            'actionUri': wsmanData.ACTIONS_URIS['get'],
            'resourceUri': self.resourceUri,
            'setting': setting,
            'extraHeader': extraHeader,
            'body': self.resource_methods['get']
        }
        response = self.request(doc = wsmanData.WS_ENVELOPE, params = params)
        if len(setting) > 0:
            response = response[self.resourceId][setting]
        return response

    def put(self, **kwargs):
        '''
        Get the current values, fill in new values and put back

        @param **kwargs: zero or more settings to put back to the wsman server
        '''
        current = self.get()
        for k, v in kwargs.iteritems():
            current[self.resourceId][k] = v
        params = {
            'uri': self.target,
            'actionUri': wsmanData.ACTIONS_URIS['put'],
            'resourceUri': self.resourceUri,
            'setting': '',
            'extraHeader': '',
            'body': current.to_xml
        }
        return self.request(doc = wsmanData.WS_ENVELOPE, params = params)

#    def delete(self, **kwargs):
#        '''
#        Delete an instance
#        '''
#        params = {
#            'uri': self.target,
#            'actionUri': ACTIONS_URIS['delete'],
#            'resourceUri': self.resourceUri,
#            'setting': '',
#            'extraHeader': '',
#            'body': self.resource_methods['delete'] % kwargs
#        }
#        return self.request(doc = WS_ENVELOPE, params = params)
#
#    def Create(self, **kwargs):
#        '''
#        Create an instance
#        '''
#        params = {
#            'uri': self.target,
#            'actionUri': ACTIONS_URIS['create'],
#            'resourceUri': self.resourceUri,
#            'setting': '',
#            'extraHeader': '',
#            'body': self.resource_methods['create'] % kwargs
#        }
#        return self.request(doc = WS_ENVELOPE, params = params)

    def enumerate(self, **kwargs):
        '''
        Return all instances of this Resource
        '''
        params = {
            'uri': self.target,
            'actionUri': wsmanData.ACTIONS_URIS['enumerate'],
            'resourceUri': self.resourceUri,
            'setting': '',
            'extraHeader': '',
            'body': self.resource_methods['enumerate'] % kwargs
        }
        enum_response = self.request(doc = wsmanData.WS_ENUM_ENVELOPE, params = params)
        params['enumctx'] = enum_response['EnumerateResponse']['EnumerationContext']
        params['actionUri'] = wsmanData.ACTIONS_URIS['pull']
        output = WryDict.WryDict({self.resourceId:[]})
        while params['enumctx']:
            data = self.request(doc = wsmanData.WS_PULL_ENVELOPE, params = params)
            if 'EnumerationContext' not in data['PullResponse']:
                params['enumctx'] = None
            output[self.resourceId].append(data['PullResponse']['Items'][self.resourceId])
        return output

    def invoke(self, method, **kwargs):
        '''
        Call a method and return the result

        @param method: the method name to call
        '''
        if method not in self.resource_methods:
            raise Exception("Method '%s' not defined" % method)
        extraHeader = ''
        if 'headerSelector' in kwargs and 'headerSelectorType' in kwargs:
            extraHeader = '<wsman:SelectorSet><wsman:Selector Name="%(headerSelectorType)s">%(headerSelector)s</wsman:Selector></wsman:SelectorSet>' % kwargs
        params = {
            'uri': self.target,
            'actionUri': self.resourceUri + "/" + method,
            'resourceUri': self.resourceUri,
            'setting': '',
            'extraHeader': extraHeader,
            'body': self.resource_methods[method] % kwargs
        }
        return self.request(doc = wsmanData.WS_ENVELOPE, params = params)

