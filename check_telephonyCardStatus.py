#!/usr/bin/env python
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

"""
Checks status of phone card and returns nagios result.
telephonyCard.getList
"""
import switchvox_common
from nagios_common import performance_data
from sv_nag_abstract import SwitchvoxNagiosInterface


NO_ALARM = 'No Alarm'
ALARM = 'Alarm'
        
class TelephonyCardStatus(SwitchvoxNagiosInterface):
    """Checks to make sure that there are no telephone card devices (T1 and analog) in alarm state.
Also checks to make sure that there is at least 1 non-alarm telephone card device being recognized by the switchvox system."""
    def __init__(self):
        pass

    def parse_options(self):
        """
        Gets generic parse options then adds whatever is necessary
        """
        parser = self._get_options_parser()

        # Default is good enough.  No need to add parser options for this check.
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
        method = "switchvox.status.telephonyCards.getList"
        parameters = None
                
        return switchvox_common.request_form(method=method, parameters=parameters)

    def _process_response_alarms(self, response):
        """
        Count alarm states returned (in response) from switchvox_request
        """
        device_list = response["response"]["result"]["devices"]["device"]
        counts = {NO_ALARM: 0, ALARM: 0}

        for device in device_list:
            state = device["state"]
            if state == NO_ALARM:
                pass
            else:
                state = ALARM
            counts[state] += 1
        return counts

    def check_condition(self, response):
        """
        Checks status and returns relevant nagios messages and codes.
        """
        alarm_states = self._process_response_alarms(response)
        errors = self.get_errors(response)

        perf_strings = []
        for label in (NO_ALARM, ALARM):
            perf = performance_data(label=label, value=alarm_states[label], mini=0)
            perf_strings.append(perf)
            
        perf_string = " |" + " ".join(perf_strings)

        if not alarm_states[NO_ALARM] >= 1:
            # 0 non-alarm channels
            return {"code": "CRITICAL", "response": "No channels available in non-alarm state" + perf_string}
        elif alarm_states[ALARM]:
            # 1 or more alarmed channels.  Really non-zero alarmed channels.
            return {"code": "WARNING", "response": "Some channels in non-alarm state" + perf_string}
        else:
            return {"code": "OK", "response": "All channels OK" + perf_string}

def main():
    telephonyCardStatus().run_nagios_check()


if __name__ == "__main__":
    main()
