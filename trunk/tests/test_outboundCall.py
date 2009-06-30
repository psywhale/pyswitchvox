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

import nose
from nose.tools import *

try:
    import json
except ImportError:
    import simplejson as json

from ..check_outboundCall import ElevatorCall 



class Error_testing(object):
    "Error testing of basic outbound call"
    
    def setUp(self):
        self.instance = ElevatorCall()
        self.instance._request_timer = 20
        self.instance.dial_first = 111111
        self.instance.timeout = 30
    
    def test_undesired_error(self):
        input = {u'response':
                    {u'errors':
                        {u'error':
                            {u'message': u'Missing required parameter (dial_as_account_id)', u'code': 10011}
                        },
                     u'method': u'switchvox.call'
                     }}
        
        test = self.instance.check_condition(input)
        
        error = input['response']['errors']['error']
        expected_message = "unexpected error code: %(code)s; error message: %(message)s" % error

        assert expected_message in test['response']


    def test_undesired_error(self):
        input = {"response" : {
                    "errors" : {
                      "error" : [
                        {
                          "code" : 10010,
                          "message" : "Invalid extension (abc). Extensions may only contain digits or *."
                        },
                        {
                          "code" : 10010,
                          "message" : "Invalid extension (def). Extensions may only contain digits or *."
                        }
                      ]
                    },
                    "method" : "switchvox.extensions.getInfo"
                  }
                }
                       
        test = self.instance.check_condition(input)
        
        expected_messages = []
        for error in input['response']['errors']['error']:
            message = "unexpected error code: %(code)s; error message: %(message)s" % error
            expected_messages.append(message)
        
        #~ error0 = input['response']['errors']['error'][0]
        #~ error1 = input['response']['errors']['error'][1]
        #~ expected_message0 = "unexpected error code: %(code)s; error message: %(message)s" % error0
        #~ expected_message1 = "unexpected error code: %(code)s; error message: %(message)s" % error1

#        print test['response']

#        print expected_message1 
#        assert False
        print test['response']
        print expected_messages

        for expected_message in expected_messages:
            assert expected_message in test['response']
        
        
class test_basic_response(object):

    def setUp(self):
        self.instance = ElevatorCall()
        self.instance._request_timer = 31
        self.instance.dial_first = 111111
        self.instance.timeout = 30
    
    def basic_test(self):
        
        input = {
                  "response" : {
                    "errors" : {
                      "error" : {
                        "code" : 41591,
                        "message" : "Your call failed to connect (Originate failed)."
                      }
                    },
                    "method" : "switchvox.call"
                  }
                }
        
        params = dict(dial_first = self.instance.dial_first, timeout=self.instance.timeout, timer=self.instance._request_timer)

        expected_message = "Call to %(dial_first)i failed (as expected) - switchvox timeout %(timeout)i sec, timer %(timer)f " % params
        
        test = self.instance.check_condition(input)
        
        print test['response']
        print expected_message
        
        
        assert expected_message in test['response']
