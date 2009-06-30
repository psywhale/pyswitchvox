#!/usr/bin/env python
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__),  os.path.pardir)))

from check_outboundCall import ElevatorCall as check

def main():
    check().run_nagios_check()

if __name__=="__main__":
    main()
