#!/usr/bin/env python

"""
Make outbound call
"""
from nagios_common import performance_data
from sv_nag_abstract import outboundCall

class ElevatorCall(outboundCall):
    """Should ring for a long while before successfully connecting.
Set timeout a little bit lower and make sure that outbound calls fail to connect.
(ie make sure calling connecting with intended phone number and long rings are happening) 
    """

    def check_condition(self, response):
        "Checks status and returns relevant nagios messages and codes."
        errors = self.get_errors(response)
        expected_errors = set([41591])

        perf_string = performance_data(label = "requestTimer",
                                       value = self._request_timer,
                                       uom = "s",
                                       mini = 0)
        perf_string = " |" + perf_string

        ####
        # Check for unexpected errors
        ####
        bad_errors = [err for err in errors if err["code"] not in expected_errors]

        base_message = "Call to %(dial_first)i %(status)s - switchvox timeout %(timeout)i sec, timer %(timer)f"
        message_params = dict(dial_first=self.dial_first, timeout=self.timeout, timer=self._request_timer)
        
        results = {}

        if bad_errors:
            # Errors we don't want
            base_err_message = "unexpected error code: %(code)s; error message: %(message)s"            
            error_message_str = "; ".join([base_err_message % err for err in bad_errors])

            results["code"] = "CRITICAL"
            message_params['status'] = "failed"
            
            base_message = error_message_str + base_message

        elif not errors:
            # No errors at all.  We want our expected errors.
            ## FIXME: Must write tests for this.
            results["code"] = "CRITICAL"
            message_params['status'] = "completed"
        
        elif self._request_timer < self.timeout:
            # Errors that we do want but timers are wrong.
            results["code"] = "CRITICAL"
            message_params['status'] = "failed before specified timeout"

        else:
            # Errors we do want.  Timers are good.
            results["code"] = "OK"
            message_params['status'] = "failed (as expected)"
        
        results["response"] = (base_message % message_params) + perf_string
        return results


class BadLineCheck(outboundCall):
    "Call to this line should fail."

    def check_condition(self, response):
        """
        Checks status and returns relevant nagios messages and codes.
        """
        errors = self.get_errors(response)
        expected_errors = set([41591])

        perf_string = performance_data(label = "requestTimer",
                                       value = self._request_timer,
                                       uom = "s",
                                       mini = 0)
                                       
        perf_string = " |" + perf_string

        ####
        # Check for unexpected errors
        ####
        bad_errors = [err for err in errors if err["code"] not in expected_errors]

        base_message = "Call to %(dial_first)i %(status)s - switchvox timeout %(timeout)i sec, timer %(timer)f"
        message_params = dict(dial_first=self.dial_first, timeout=self.timeout, timer=self._request_timer)
        
        results = {}

        if bad_errors:
            # Errors we don't want
            base_err_message = "unexpected error code: %(code)s; error message: %(message)s"            
            error_message_str = "; ".join([base_err_message % err for err in bad_errors])

            results["code"] = "CRITICAL"
            message_params['status'] = "failed"
            
            base_message = error_message_str + base_message

        elif not errors:
            # No errors at all.  We want our expected errors.
            ## FIXME: Must write tests for this.
            results["code"] = "CRITICAL"
            message_params['status'] = "completed"
        
        else:
            # Errors we do want.  Timers are good.
            results["code"] = "OK"
            message_params['status'] = "failed (as expected)"
        
        results["response"] = (base_message % message_params) + perf_string
        return results

class GoodLineCheck(outboundCall):
    """Check that regular outbound call is able to connect with no issues.
If you direct it to call internal numbers it can test your inbound capabilities as well."""

    def check_condition(self, response):
        """
        Checks status and returns relevant nagios messages and codes.
        """
        perf_string = performance_data(label = "requestTimer",
                                       value = self._request_timer,
                                       uom = "s",
                                       mini = 0)
        perf_string = " |" + perf_string

        message_params = dict(dial_first=self.dial_first, timeout=self.timeout, timer=self._request_timer)
        base_message = "Call to %(dial_first)i %(status)s - switchvox timeout %(timeout)i sec, timer %(timer)f"
        
        results = {}

        errors = self.get_errors(response)
        
        if errors:
            # Errors we don't want
            base_err_message = "unexpected error code: %(code)s; error message: %(message)s"            
            error_message_str = "; ".join([base_err_message % err for err in errors])

            base_message = error_message_str + base_message

            results["code"] = "CRITICAL"
            message_params['status'] = "failed"
    
        else:
            results["code"] = "OK"
            message_params['status'] = "completed"
    
        results["response"] = (base_message % message_params) + perf_string
        return results
        
def main():
#    xx = ElevatorCall()
    xx = GoodLineCheck()
#    xx = BadLineCheck()
    xx.run_nagios_check()



if __name__ == "__main__":
    main()
