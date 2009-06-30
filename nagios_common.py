"""
Nagios common
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
import sys
import optparse

nagios_codes = {'OK': 0, 
                'WARNING': 1, 
                'CRITICAL': 2,
                'UNKNOWN': 3}
				
def nagios_return(code, response):
    """ prints the response message
        and exits the script with one
        of the defined exit codes
        DOES NOT RETURN 
    """
    print(code + ": " + response)
    sys.exit(nagios_codes[code])


def get_options_parser():
    parser = optparse.OptionParser("usage: %prog [options]")

    parser.add_option("-H", "--host", dest="hostname",
                       type="string", help="specify hostname to run on")
    
    parser.add_option("", "--password", dest="password",
                        type="string", help="specify password")

    parser.add_option("", "--username", dest="username", default="admin",
                        type="string", help="specify username")

    return parser

    #~ (options, args) = parser.parse_args()
#~ 
    #~ return options, args

def parse_options():
    #~ parser = optparse.OptionParser("usage: %prog [options]")
#~ 
    #~ parser.add_option("-H", "--host", dest="hostname",
                       #~ type="string", help="specify hostname to run on")
    #~ 
    #~ parser.add_option("", "--password", dest="password",
                        #~ type="string", help="specify password")
#~ 
    #~ parser.add_option("", "--username", dest="username", default="admin",
                        #~ type="string", help="specify username")

    parser = get_options_parser()
    
    (options, args) = parser.parse_args()

    return options, args
    

def performance_data(label, value, uom="", warn="", crit="", mini="", maxi=""):
    """
    defined here: http://nagiosplug.sourceforge.net/developer-guidelines.html#AEN201
    """
    formatted_string = "%(label)s=%(value)s%(uom)s;%(warn)s;%(crit)s;%(mini)s;%(maxi)s" % locals()

    # Get rid of spaces
    formatted_string = "".join(formatted_string.split())
    
    return formatted_string
