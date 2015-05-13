#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: binary -*-

import os
import sys
from time import sleep
from shutil import copytree

# TO:DO
# Add auto-uninstall method.

loginname = os.getlogin()
projectpath = os.path.dirname(os.path.abspath(__file__))
projectname = projectpath.split('/')[-1]
destinedpath = '/usr/local/bin/{}'.format(projectname)
symlinkdest = '/usr/local/bin/'

def rootcheck():
    if os.getuid() != 0:
        print "\nRun as root! to install {} to your /usr/local/bin/ directory.\n".format(projectname)
        exit(0)

def main(sln):

    print "\nInstalling {} to /usr/local/bin/{}".format(projectname, sln)
    sleep(1)
    # Copy the current directory to the dest path
    copytree(projectpath, destinedpath)
    os.system('sudo ln -s {} {}'.format(destinedpath + '/crippled.py', symlinkdest + '/{}'.format(sln)))
    os.system('sudo chmod a+rw -R {}'.format(destinedpath))
    os.system('sudo chown -R {} {}'.format(loginname, destinedpath))

    # Successful message.
    print "installed {} successfully!, try '{}' from a different directory".format(projectname, sln)
    # Uninstall message
    print "To uninstall {} go to your {} directory and remove {}, {}.\n".format(projectname, symlinkdest, destinedpath, sln)

if __name__ == '__main__':
    # Quick root check.
    rootcheck()

    try:
        try:
            main(sys.argv[1])
        except IndexError, e:
            print "\n Provide a syslink name for {}".format(projectname)
            print " Usage: sudo ./install [NAME]\n"
    except OSError, e:
        pass
        if 'File exists' in e:
            print "To uninstall {} go to your {} directory and remove {}, {}.\n".format(projectname, symlinkdest, destinedpath, sys.argv[1])
