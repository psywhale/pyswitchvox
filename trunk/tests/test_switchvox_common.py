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
from .. import switchvox_common



class Test_Error_Codes(object):
    def test_basic_error_read(self):
        input = {u'response':
            {u'errors':
                {u'error': {u'code': 10011, u'message': u'Missing required parameter (dial_as_account_id)'}},
            u'method': u'switchvox.call'}}
        
        
        expected = [{'code': 10011, 'message': 'Missing required parameter (dial_as_account_id)'}]
        tested = switchvox_common.get_errors(response=input)
        
        assert_equal(tested, expected)
    
    
    def test_multiple_errors(self):
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
        
        expected = [{"code" : 10010, "message" : "Invalid extension (abc). Extensions may only contain digits or *."},
                    {"code" : 10010, "message" : "Invalid extension (def). Extensions may only contain digits or *."}
                    ]
        tested = switchvox_common.get_errors(response=input)
        
        assert_equal(tested, expected)



    def test_no_errors(self):
        input = {"response" : {
                    "method" : "switchvox.extensions.getInfo",
                    "result" : {
                      "extensions" : {
                        "extension" : {
                          "email_address" : "name@example.com",
                          "template_name" : "Default",
                          "template_id" : 1,
                          "number" : 222,
                          "status" : 1,
                          "date_created" : "2009-06-12 18:21:26",
                          "type_display" : "SIP Extension",
                          "account_id" : 1111,
                          "display" : "Firstname Lastname",
                          "last_name" : "Lastname",
                          "type" : "sip",
                          "can_dial_from_ivr" : 1,
                          "first_name" : "Firstname"
                        }
                      }
                    }
                  }
                }

        expected = []
        tested = switchvox_common.get_errors(response=input)
        assert_equal(tested, expected)
