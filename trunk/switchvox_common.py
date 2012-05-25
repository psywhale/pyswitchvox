"""
Switchvox common methods
"""
import urllib2

try:
    import json
except ImportError:
    import simplejson as json


def switchvox_request(username, password, json_req, hostname):
    url = "https://%s" % hostname

    #create a password manager
    passManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passManager.add_password(None, url, username, password)

    #setup auth handler and opener
    authHandler = urllib2.HTTPDigestAuthHandler(passManager)
    urlOpener = urllib2.build_opener(authHandler)

    #set http headers
    urlOpener.add_headers={'Host:':hostname ,'Content-Type': 'text/json','Content-Length':str(len(json_req))}

    #send request
    req = urlOpener.open(url+"/json",data=json_req)

    #read and return result
    result=req.read()
    return result

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
