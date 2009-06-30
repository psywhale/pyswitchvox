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
import sys
import time
import nagios_common
import switchvox_common
import logging

logging.basicConfig(level=logging.WARNING)

class SwitchvoxNagiosInterface(object):
    """
    Basic, standard, foundatoin of switchvox-nagios plugin object.
    """
    # Set it as a class variable.  Should be more than fine.

    @classmethod
    def _get_options_parser(cls):
        parser = nagios_common.get_options_parser()
    
        parser.set_description(cls.__doc__)

        return parser
    
    def _parser_cleanup(self, parser):
        if not sys.argv[1:]:
            parser.print_help()
            sys.exit(3)
    
    def get_errors(cls, response):
        return switchvox_common.get_errors(response=response)

    def _get_response(self):
        requester = switchvox_common.switchvox_request
        response = requester(username=self.username,
                             password=self.password,
                             json_req=self.generate_req(),
                             hostname=self.hostname)
        return response
    
    def generate_req(self):
        """
        Generates request object based on parse options results.
        """
        raise NotImplementedError
    
    def run_nagios_check(self):
        # Populates necessary variables to instance.
        parser = self.parse_options()
        self._parser_cleanup(parser)

        start = time.time()
        response = self._get_response()
        logging.debug(response)
        end = time.time()
        self._request_timer = end - start
        
        nagios_common.nagios_return(**self.check_condition(response))



class outboundCall(SwitchvoxNagiosInterface):
    """
    Abstract class that defines majority of stuff to make outbound call.
    Only thing missing is specific check conditions.  ie what qualifies as success or failure.
    """
    def __init__(self):
        pass

    def parse_options(self):
        """
        Gets generic parse options then adds whatever is necessary
        """
        parser = self._get_options_parser()

        parser.add_option("", "--dial_first", dest="dial_first",
                           type="int", help="number to dial first")

        parser.add_option("", "--dial_second", dest="dial_second",
                           type="int", help="number to dial second")

        parser.add_option("", "--timeout", dest="timeout", default=20,
                           type="int", help="call timeout to send to switchvox")
        
        parser.add_option("", "--dial_as_account_id", dest="dial_as_account_id",
                           type="int", help="account id to use for dial")
                           
        (options, args) = parser.parse_args()

        ###
        # Set all options as attributes of instance self.
        ###
        for key in parser.defaults.keys():
            option_value = getattr(options, key)
            setattr(self, key, option_value)
        
        return parser

    def generate_req(self):
        """
        Generates request object based on parse options results.
        """
        method = "switchvox.call"
        parameters = {"ignore_user_call_rules": "1",
                      "ignore_user_api_settings": "1",
                      "timeout": self.timeout,
                      "dial_as_account_id": self.dial_as_account_id,
                      "dial_first": self.dial_first,
                      "dial_second": self.dial_second}

        return switchvox_common.request_form(method=method, parameters=parameters)

    def check_condition(self, response):
        """
        Checks status and returns relevant nagios messages and codes.
        """
        raise NotImplementedError
