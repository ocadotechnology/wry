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

import sys
import os
import wry
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

'''
Created on 12 Jul 2017

@author: adrian
'''

class CLITool(object):
    '''
    Base class for all wry CLI tools.

    It just makes the code simpler
    '''
    name = os.path.basename(sys.argv[0])
    version = "v0.0"
    build_date = "never"
    short_desc = __import__('__main__').__doc__.split("\n")[1]
    copyright = "Copyright 2017 Ocado Technology. All Rights Reserved."
    licence = '''
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.
'''
    _debug = True
    _showxml = False

    def __init__(self):
        '''
        Set up the environment for the CLI tool.

        Add extra init in __extra_init__ below
        '''
        version_message = '%%(prog)s %s (%s)' % (
            self.version,
            self.build_date
        )
        help_message = "%s\n\n  %s\n\n%s\n\nUSAGE\n" % (
            self.short_desc,
            self.copyright,
            self.licence
        )
        try:
            self.parser = ArgumentParser(
                description = help_message,
                formatter_class = RawDescriptionHelpFormatter
            )
            # Setup argument parser
            self.parser.add_argument("-H", "--host", dest = "host", help = "host to connect to. [default: %(default)s]", metavar = "name/ip", required = True)
            self.parser.add_argument("-s", "--ssl", action = "store_true", dest = "ssl", help = "connect using ssl. [default: %(default)s]", default = False)
            self.parser.add_argument("-n", "--name", dest = "name", help = "name to login as. [default: %(default)s]", metavar = "name", required = True)
            self.parser.add_argument("-p", "--password", dest = "password", help = "login password. [default: %(default)s]", metavar = "password", required = True)
            # Get extra settings from the CLI app
            self.extra_init()
            # Add debug options last
            self.parser.add_argument('-V', '--version', action = 'version', version = version_message)
            self.parser.add_argument("-d", "--debug", dest = "debug", action = "store_true", help = "enable debugging")
            self.parser.add_argument("-x", "--showxml", dest = "showxml", action = "store_true", help = "show inbound and outbound XML")

            # Process arguments
            args = self.parser.parse_args()

            # Grab some things
            self._debug = args.debug != False
            self._showxml = args.showxml != False
            self.host = args.host
            self.name = args.name
            self.password = args.password
            self.dev = wry.AMTDevice(
                target = self.host,
                is_ssl = args.ssl,
                username = self.name,
                password = self.password,
                debug = self.debug,
                showxml = self.showxml
            )
            # Do extra parsing
            self.extra_parse(args)
        except KeyboardInterrupt:
            ### handle keyboard interrupt ###
            pass
        except Exception, e:
            if self.debug:
                raise
            indent = len(self.name) * " "
            sys.stderr.write(self.name + ": " + repr(e) + "\n")
            sys.stderr.write(indent + "  for help use --help\n\n")

    def run(self):
        try:
            return self.extra_run()
        except KeyboardInterrupt:
            ### handle keyboard interrupt ###
            return 0
        except Exception, e:
            if self.debug:
                raise
            indent = len(self.name) * " "
            sys.stderr.write(self.name + ": " + repr(e) + "\n")
            sys.stderr.write(indent + "  for help use --help\n\n")
            return 2

    def extra_init(self):
        '''
        Override to add extra intialisation
        '''
        pass

    def extra_parse(self, args):
        pass

    def extra_run(self):
        pass

    @property
    def debug(self):
        return self._debug

    @property
    def showxml(self):
        return self._showxml
