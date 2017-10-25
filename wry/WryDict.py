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

import xmltodict
import json
from ast import literal_eval
from collections import OrderedDict
import wsmanData

"""
Wry data structures and helpers.
"""


class WryDict(OrderedDict):
    '''An OrderedDict with the ability to be generated from wman-returned XML'''

    def __init__(self, *args, **kwargs):
        self._from_xml = False
        super(WryDict, self).__init__(*args, **kwargs)

    def dump(self, depth = ''):
        return json.dumps(self, indent = 2)

    @property
    def to_xml(self):
        '''
        Return the XML representation of this WryDict
        '''
        def _convert_values(input_dict):
            '''
            Convert values from Python to XML friendly
            '''
            # TODO: add an ns_uri kwarg so we can specify a namespace if one is not here...
            output = self.__class__()
            for key, value in input_dict.iteritems():
                try:
                    value = _convert_values(value)
                except AttributeError:
                    if value is None:
                        continue # Omit this tag - fixes issues with passwords, could possibly cause them elsewhere?
                    if value in (True, False):
                        value = unicode(value).lower()
                    else:
                        value = unicode(value)
                output[key] = value
            return output

        def _with_namespaces():
            '''
            Add an XML namespace attribute(s) to the dictionary value(s).
            '''
            output = self.__class__()
            for resource_name, resource in self.iteritems():
                uri = wsmanData.RESOURCE_URIS.get(resource_name, None)
                output[resource_name] = resource.copy()
                output[resource_name][u'@xmlns'] = uri
            return output
        #TODO: Make this clearer and better and more integrated an stuff.
        output = _convert_values(_with_namespaces())
        _xml = xmltodict.unparse(output, full_document = False, pretty = False)
        return _xml

    @classmethod
    def from_xml(cls, xmlstr):
        '''
        Construct a WryDict from an XML string
        '''
        def _strip_namespace_prefixes(input_dict):
            '''
            Given a dict-like object, perhaps containing dict-like objects to an arbitary
            depth, return a copy with XML namespace prefixes stripped from each
            dict[like-object]'s keys.
            '''
            if not isinstance(input_dict, dict):
                return None
            outdict = cls()
            for key, value in input_dict.iteritems():
                key = key.split(':')[-1]
                value = _strip_namespace_prefixes(value) or value
                outdict[key] = value
            return outdict
        mydict = xmltodict.parse(xmlstr, process_namespaces = False)
        mydict = _strip_namespace_prefixes(mydict)
        body = mydict[u'Envelope'][u'Body']
        outdict = cls()
        for key, value in body.values()[0].iteritems():
            if value in (u'true', u'false'):
                value = value.capitalize()
            try:
                value = literal_eval(value)
            except (SyntaxError, ValueError):
                pass
            outdict[key] = value
        self = cls({body.keys()[0]: outdict})
        self._from_xml = True
        return self

    @property
    def error(self):
        if self.source_doc.is_fault():
            return self.source_doc.fault().reason()
        else:
            return None

    def __repr__(self):
        items = ''
        if self._from_xml:
            bookends = ['<{', '}>']
        else:
            bookends = ['-{', '}-']
        for key, value in self.iteritems():
            items += '%r: %r, ' % (key, value)
        return bookends[0] + items + bookends[-1]

    def as_json(self, indent = 4):
        return json.dumps(self, indent = indent)
