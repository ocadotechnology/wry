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
Common functionalities for AMT Driver
"""
import logging
import pywsman
import xmltodict
from ast import literal_eval
from xml.etree import ElementTree
from wry import data_structures
from wry import exceptions
from wry.decorators import retry, add_client_options
from wry.config import RESOURCE_URIs
from wry.data_structures import _strip_namespace_prefixes, WryDict



_SOAP_ENVELOPE = 'http://www.w3.org/2003/05/soap-envelope'

LOG = logging.getLogger(__name__)

AMT_PROTOCOL_PORT_MAP = {
    'http': 16992,
    'https': 16993,
}


def _validate(doc, silent=False):
    if doc is None:
        raise exceptions.AMTConnectFailure
    if not silent:
        if doc.is_fault():
            raise exceptions.WSManFault(doc)
    return doc


@add_client_options
@retry
def wsman_get(client, resource_uri, options=None, silent=False):
    '''Get target server info'''
    doc = client.get(options, resource_uri)
    return _validate(doc, silent=silent)


@add_client_options
@retry
def wsman_pull(client, resource_uri, options=None, wsman_filter=None, context=None, silent=False):
    '''Get target server info'''
    doc = client.pull(options, wsman_filter, resource_uri, context)
    return _validate(doc, silent=silent)


@add_client_options
@retry
def wsman_enumerate(client, resource_uri, options=None, wsman_filter=None, silent=False):
    '''Get target server info'''
    doc = client.enumerate(options, wsman_filter, resource_uri)
    return _validate(doc, silent=silent)


@add_client_options
@retry
def wsman_put(client, resource_uri, data, options=None, silent=False):
    '''Invoke method on target server
    :param silent: Ignore WSMan errors, and return the document anyway. Does not
    ignore the endpoint being down.
    '''
    doc = client.put(options, resource_uri, str(data), len(data))
    return _validate(doc, silent=silent)

@add_client_options
@retry
def wsman_invoke(client, resource_uri, method, data=None, options=None, silent=False):
    '''Invoke method on target server.'''
    doc = client.invoke(options, resource_uri, str(method), pywsman.create_doc_from_string(str(data)))
    return _validate(doc, silent=silent)


def get_resource(client, resource_name, options=None):
    '''
    '''
    uri = RESOURCE_URIs[resource_name]
    doc = wsman_get(client, uri, options=options)
    return WryDict(doc)
 

def enumerate_resource(client, resource_name, wsman_filter=None, options=None):
    '''
    class.
    '''
    uri = RESOURCE_URIs[resource_name]
    doc = wsman_enumerate(client, uri, options=options) # Add in relevant kwargs... filter?
    doc = WryDict(doc)
    context = doc['EnumerateResponse']['EnumerationContext']
    ended = False
    output = {resource_name: []}
    while ended is False:
        doc = wsman_pull(client, uri, context=str(context), options=options)
        response = WryDict(doc)['PullResponse']
        ended = response.pop('EndOfSequence', False)
        output[resource_name].append(response['Items'][resource_name])
    return output


def put_resource(client, indict, options=None, uri=None, silent=False):
    '''
    Given a dict or  describing a wsman resource, post this resource to the client.
    :returns: data_structures.WryDict
    :param indict: A dictionary or dictionary-like object (eg.
    common.RESOURCE_URIs.
    :param uri: If a mapping does not exist in common.RESOURCE_URIs, the resource URI can be specified manually here.
    :param mappings: A dictionary providing extra mappings between resource names and URIs.
    '''
    if not uri:
        uri = RESOURCE_URIs[indict.keys()[0]] # Possible to support multiple simply here?
    data = indict.as_xml()
    doc = wsman_put(client, uri, data, options=options, silent=silent)
    return WryDict(doc)


def invoke_method(client, method, input_dict, options=None):
    resource_name = input_dict.keys()[0]
    input_dict = WryDict(input_dict).with_namespaces()
    data = input_dict[resource_name]
    uri = data.pop(u'@xmlns')
    data.values()[0][u'@xmlns'] = uri
    xml = xmltodict.unparse(data, full_document=False, pretty=True)
    doc = wsman_invoke(client, RESOURCE_URIs[resource_name], method, xml, options=options)
    returned = WryDict(doc)
    return_value = returned[returned.keys()[0]]['ReturnValue']
    if return_value != 0:
        raise exceptions.NonZeroReturn(return_value)
    return returned

