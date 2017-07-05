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

"""
Wry data structures and helpers.
"""

import xmltodict
import json
from ast import literal_eval
from collections import OrderedDict# as NormalOrderedDict
from wry.config import RESOURCE_URIs


class WryDict(OrderedDict):
    '''An OrderedDict with the ability to be generated from wman-returned XML'''

    def __init__(self, *args, **kwargs):
        self.from_xml = False
        try:
            super(WryDict, self).__init__(*args, **kwargs)
        except (TypeError, ValueError) as original_exception:
            self.source_doc = args[0]
            try:
                data = self._from_xmldoc(self.source_doc)
                super(WryDict, self).__init__(**data)
            except: # Invalid XmlDoc or XML string...
                raise original_exception
            else:
                self.from_xml = True

    def as_xml(self):
        '''TODO: Make this clearer and better and more integrated an stuff.'''
        output = self.with_namespaces()
        output = _convert_values(output)
        _xml = xmltodict.unparse(output, full_document=False, pretty=False)
        return _xml

    def with_namespaces(self):
        '''Add an XML namespace attribute(s) to the dictionary value(s).'''
        output = OrderedDict()
        for resource_name, resource in self.iteritems():
            uri = RESOURCE_URIs.get(resource_name, None)
            output[resource_name] = resource.copy()
            output[resource_name][u'@xmlns'] = uri
        return output

    @property
    def error(self):
        if self.source_doc.is_fault():
            return self.source_doc.fault().reason()
        else:
            return None

    def _from_xmldoc(self, doc):
        mydict = xmltodict.parse(doc.root().string(), process_namespaces=False)
        # .root() as opposed to .body() because they both seem to return the same thing:
        mydict = _strip_namespace_prefixes(mydict)
        body = mydict[u'Envelope'][u'Body']
        outdict = WryDict()
        for key, value in body.values()[0].iteritems():
            if value in (u'true', u'false'):
                value = value.capitalize()
            try:
                value = literal_eval(value)
            except (SyntaxError, ValueError):
                pass
            outdict[key] = value
        return {body.keys()[0]: outdict}

    def __repr__(self):
        items = ''
        if self.from_xml:
            bookends = ['<{', '}>']
        else:
            bookends = ['-{', '}-']
        for key, value in self.iteritems():
            items += '%r: %r, ' % (key, value)
        return bookends[0] + items + bookends[-1]

    def as_json(self, indent=4):
        return json.dumps(self, indent=indent)


def _convert_values(input_dict):
    '''
    TODO: add an ns_uri kwarg so we can specify a namespace if one is not
    here...
    '''
    output = OrderedDict()
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
        


def _strip_namespace_prefixes(input_dict):
    '''
    Given a dict-like object, perhaps containing dict-like objects to an arbitary
    depth, return a copy with XML namespace prefixes stripped from each
    dict[like-object]'s keys.
    '''
    try:
        # Trigger an AttributeError if the input is not dict-like:
        outdict = input_dict.copy()
        outdict.clear()
    except AttributeError:
        return None
    for key, value in input_dict.iteritems():
        key = key.split(':')[-1]
        value = _strip_namespace_prefixes(value) or value
        outdict[key] = value
    return outdict
