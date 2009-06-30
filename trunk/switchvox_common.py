"""
Switchvox common methods
"""
import subprocess
from subprocess import PIPE

try:
    import json
except ImportError:
    import simplejson as json


def switchvox_request(username, password, json_req, hostname):
    url = "https://%s/json" % hostname
    p = subprocess.Popen(['/usr/bin/wget', '--no-check-certificate',
                        '--http-user', username,
                        '--http-password', password,
                        '--header', 'Content-Type: text/json',
                        '--post-data', json_req, url, '-O', '-',
    #                    '--post-data', req, url, '-O', fifopath,
                        ], stdout=PIPE, stderr=PIPE)
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
