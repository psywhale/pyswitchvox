"""
Switchvox common methods
"""
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import subprocess
from subprocess import PIPE

try:
    import json
except ImportError:
    import simplejson as json


def switchvox_request(username, password, json_req, hostname):
    url = "https://%s/json" % hostname
    p = subprocess.Popen(['wget', '--no-check-certificate',
                        '--http-user', username,
                        '--http-password', password,
                        '--header', 'Content-Type: text/json',
                        '--post-data', json_req, url, '-O', '-',
    #                    '--post-data', req, url, '-O', fifopath,
                        ], stdout=PIPE, stderr=PIPE
                        universal_newlines=True) # Allows forward-compatibility with python3+
    wget_result = json.load(p.stdout)
    
    return wget_result

def get_errors(response):
    """
    Returns processed list of errors from switchvox response
    example output:
            expected = [{'code': 10011, 'message': 'Missing required parameter (dial_as_account_id)'}]
            
            expected = [{"code" : 10010, "message" : "Invalid extension (abc). Extensions may only contain digits or *."},
                        {"code" : 10010, "message" : "Invalid extension (def). Extensions may only contain digits or *."}
                        ]            
    """
    ####
    # Check for no errors at all
    ####
    try:
        error = response['response']['errors']['error']
    except KeyError:
        return []

    ####
    # Test for single error situation.
    ####
    try:
        items = error.items()
    except AttributeError:
        # Multiple error situation.
        # 'error' is list object. Each 'err' is a single error dict.
        return [err for err in error]
    else:
        # 'error' is dict object: single error situation.
        return [error]
    
def request_form(method, parameters=None):
    if not parameters:
        parameters = {}
    parameters = dict(parameters)
    
    request = {"request": {
                 "version": "17487",
                 "method": method,
                 "parameters": parameters}}

    return json.dumps(request)
