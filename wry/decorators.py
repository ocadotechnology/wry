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

from functools import wraps
from time import sleep
import pywsman
from wry.config import CONNECT_RETRIES
from wry.exceptions import AMTConnectFailure



def retry(infunc):
    @wraps(infunc)
    def newfunc(*args, **kwargs):
        for _ in range(CONNECT_RETRIES + 1):
            try:
                return infunc(*args, **kwargs)
            except AMTConnectFailure:
                sleep(.1)
            except:
                break
        raise
    return newfunc
 

def add_client_options(infunc):
    @wraps(infunc)
    def newfunc(*args, **kwargs):
        options = kwargs.pop('options', None) or pywsman.ClientOptions()
        return infunc(*args, options=options, **kwargs)
    return newfunc

