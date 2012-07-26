denyGen
=======

Generates a hosts.deny file to block spam and/or countries

Run `denyGen.py --help` for help.

Suggested use with root cron (after moving denyGen.py to /usr/local/bin/):
`0 6 * * * /usr/local/bin/denyGen.py --spam 30 --country cn --output /etc/hosts.deny`

The above exapmle will generate a new host.deny at 6am everyday blocking spammer from the last 30 days and blocking China.

Visit http://www.stopforumspam.com/ for informataion about the spam block list.
Visit http://www.ipdeny.com/ipblocks/ for information about the contry block lists.