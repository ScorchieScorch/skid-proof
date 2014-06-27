#!/usr/bin/env python

'''
shell_kill.py

Monitors the process list for specific processes started by specific users
and kills any that match

This is typically used to prevent an exploit from successfully launching a
shell or starting nc

This script requires psutil, on Debian / Ubuntu, it can be installed using:

#apt-get install python-psutil

On other distributions use:

#pip install psutil
'''

import psutil, time, getpass

#List of processes to kill, these are regex search
#patterns
DISALLOWED_PROCS = [
    "sh.*",
    "nc .*",
    "netcat.*",
    ]

#List of users to check for disallowed processes
DISALLOWED_USERS = [
    "www-data"
    ]

#This script should be run as root or as a user with permission to kill
#these processes
if getpass.getuser != 'root':
    print 'This script should be run as root. Continuing anyways.'

while True:
    time.sleep(1)
    for proc in psutil.process_iter():
        if proc.username in DISALLOWED_USERS:
            for pat in DISALLOWED_PROCS:
                m = re.search(pat, proc.name)
                if m:
                    try:
                        #Pattern matched! Kill it!
                        proc.kill()
                        print "Process Killed! " + str(proc.pid) + ", " + proc.username + " " + proc.name
                    except psutil.AccessDenied:
                        print "Could not kill " + str(proc.pid) + ", \'" + proc.name + "\' Access Denied."
