#!/usr/bin/env python

import irrtoolib
import sys

if len(sys.argv) < 5:
   print "give as args: ripe-obj, rou-obj, rou_type, job_type(black whole|no black whole)"
   print "eg. python get_prefixes.py AS-2K YOUR-ROUTER-POLICY-NAME junos|cisco_xr Y|N"
   sys.exit()

ripe_obj = sys.argv[1]
rou_obj = sys.argv[2]
rou_typ = sys.argv[3]
job_typ = sys.argv[4]

pref = irrtoolib.asset_obj_ripe(ripe_obj)
policy = ''

print "----------><----------><------------><-----------><----------><------------><-----------"

if rou_typ == 'junos' and job_typ == 'N':
   junos_n = irrtoolib.juniper_no_bh(pref,rou_obj)
   policy = ('\n').join(junos_n)

if rou_typ == 'junos' and job_typ == 'Y':
   junos_y = irrtoolib.juniper_bh(pref,rou_obj)
   policy = ('\n').join(junos_y)

if rou_typ == 'cisco_xr' and job_typ == 'N':
   cisco_n = irrtoolib.r_xr(pref, rou_obj, 'N', rou_obj)
   policy = ('\n').join(cisco_n)

if rou_typ == 'cisco_xr' and job_typ == 'Y':
   cisco_y = irrtoolib.r_xr(pref, rou_obj, 'Y', rou_obj)
   policy = ('\n').join(cisco_y)

print policy
print "----------><----------><------------><-----------><----------><------------><-----------"
