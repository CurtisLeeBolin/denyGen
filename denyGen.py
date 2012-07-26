#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  denyGen.py
#
#  Generates a hosts.deny file to block spam and/or countries
#
#  Copyright 2012 Curtis Lee Bolin <curtlee2002@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import argparse, re, urllib.request, zipfile

def CheckArgs():
    parser = argparse.ArgumentParser(
        prog='denyGen.py',
        description='A hosts.deny Generator',
        epilog='Copyright 2012 Curtis lee Bolin <curtlee2002@gmail.com>')
    parser.add_argument('-c', '--country',
        dest='countries',
        help='a comma separated list of countries to block')
    parser.add_argument('-s', '--spam',
        dest='days',
        help='adds spam blocklist (number of days can be 1, 7, 30, 90, 180, or 365)')
    parser.add_argument('-o', '--output',
        dest='output',
        default='hosts.deny',
        help='output file (default: hosts.deny)')
    args = parser.parse_args()
    if not (args.countries or args.days):
        print('Spam and/or Country must be selected.  Try --help for help.')
        exit(1)
    daysList = ['1', '7', '30', '90', '180', '365']
    if args.days not in daysList:
        print('Days parameter is incorrect check --help')
        exit(1)
    return args

def runCountries(args):
    countryList = []
    if args.countries:
        for item in args.countries.split(','):
            COUNTRY_LIST = 'http://www.ipdeny.com/ipblocks/data/countries/' + item + '.zone'
            local_filename, headers = urllib.request.urlretrieve(COUNTRY_LIST)
            countryIPs = open(local_filename).read()
            countryIpList = []
            countryIpMatch = re.compile(r'\d+\.\d+\.\d+\.\d+\/\d+')
            for countryIP in countryIPs.__str__().split('\n'):
                if countryIpMatch.match(countryIP):
                    countryIpList.append(countryIP)
            args.countryIpList = countryIpList

def runSpam(args):
    if args.days:
        SPAM_LIST = 'http://www.stopforumspam.com/downloads/listed_ip_' + args.days + '.zip'
        SPAM_LIST_FILENAME = 'listed_ip_' + args.days + '.txt'
        local_filename, headers = urllib.request.urlretrieve(SPAM_LIST)
        z = zipfile.ZipFile(local_filename, 'r')
        spamIPs = z.read(SPAM_LIST_FILENAME).__str__()
        spamIpList = []
        spamIpMatch = re.compile(r'\d+\.\d+\.\d+\.\d+')
        for spamIP in spamIPs.split('\\n'):
            if spamIpMatch.match(spamIP):
                spamIpList.append(spamIP)
        args.spamIpList = spamIpList

def saveOutput(args):
    HOSTS_DENY_FILENAME = args.output
    deny_file = open(HOSTS_DENY_FILENAME, 'w')
    if args.days:
        deny_file.write('# Blocking the last ' + args.days + ' days Spamming IPs\n')
        for spamIP in args.spamIpList:
            deny_file.write('ALL: ' + spamIP + '\n')
        deny_file.write('\n\n')
    if args.countries:
        deny_file.write('# Blocking Counties ' + args.countries + '\n')
        for countryIP in args.countryIpList:
            deny_file.write('ALL: ' + countryIP + '\n')
        deny_file.write('\n\n')
    deny_file.close()

def main():
    args = CheckArgs()
    runCountries(args)
    runSpam(args)
    saveOutput(args)
    return 0

if __name__ == '__main__':
    main()
