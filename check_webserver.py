#!/usr/bin/python

import subprocess
import sys


def check_webserver():
    cmd = 'ps -A | grep nginx | grep -v grep'
    # ps shows currently running processes, -a for all users. grep searches for -v lines that do not match nginx

    (status, output) = subprocess.getstatusoutput(cmd)

    if status == 0:
        print('Nginx is already running on this instance\n')
        sys.exit(1)
    else:
        sys.stderr.write(output) # stderr handles almost all of the interpreters error messages
        print(status)
        print('Nginx is not currently running on this instance.\nStarting Nginx now...\n')
        cmd = 'sudo service nginx start'
        (status, output) = subprocess.getstatusoutput(cmd)
        if status == 0:
            print('Unable to run Nginx')
            sys.exit(2)
        else:
            print('Nginx is now up and running')
            sys.exit(0)


# Standard boilerplate that calls the main() function.
def main():
    check_webserver()


if __name__ == '__main__':
    main()
