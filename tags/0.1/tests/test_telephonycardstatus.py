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

from .. import check_telephonyCardStatus



class Basic_tests(object):
    
    def first_test(self):
        
        test = check_telephonyCardStatus.TelephonyCardStatus().generate_req()
        expected = '{"request": {"method": "switchvox.status.telephonyCards.getList", "version": "17487", "parameters": {}}}'

        expected = json.loads(expected)
        
        assert_equals(json.loads(test), expected)

