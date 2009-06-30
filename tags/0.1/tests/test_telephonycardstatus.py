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

