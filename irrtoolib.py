import re
import subprocess

def cip(ip):
    regex = '^\d+\.\d+\.\d+\.\d+\/\d+$'
    if re.match(regex, ip) is not None:
        return 1
    else:
        return 0

def r_xr(prefixes, rou, typ, ron):
    routstoconf = prefixes
    host = rou
    type_ = 'cisco_xr'
    router_obj_name = ron
    bh_type = typ

    out = []

    ss = "  "
    if bh_type == 'Y':
        out.append( 'prefix-set ' + router_obj_name)
        gg = str(32)
        for el in routstoconf:
            if not cip(el):
                gg = str(128)
            if routstoconf[-1] == el:
                out.append( ss + el + " ge " + gg)
            else:
                out.append( ss + el + " ge " + gg + ",")
            gg = str(32)

        out.append('end-set')

    elif bh_type == 'N':
        out.append('prefix-set ' + router_obj_name)
        for el in routstoconf:
            if routstoconf[-1] == el:
                out.append(ss + el)
            else:
                out.append(ss + el + ",")
        out.append('end-set')

    return out

def juniper_bh(pset,pname):
    ret = []
    PN = "BH-" + str(pname)
    ret.append("delete policy-options policy-statement " + PN)
    ret.append("set policy-options policy-statement " + PN + " term 1a apply-groups blackhole")
    typ = "/32-/32"
    check = 0
    for item in pset:
        if re.match("^.*\:.*", item):
            typ = "/128-/128"
	    ret.append("set policy-options policy-statement " + PN + " term 1b apply-groups blackhole")
	    ret.append("set policy-options policy-statement " + PN + " term 1b from family inet6")
	    ret.append("set policy-options policy-statement " + PN + " term 1b from route-filter " + str(item) + " prefix-length-range " + str(typ))
	    check = 1
        else:
            typ = "/32-/32"
	    ret.append("set policy-options policy-statement " + PN + " term 1a from route-filter " + str(item) + " prefix-length-range " + str(typ))

    typ = "/24"
    for item in pset:
        if re.match("^.*\:.*", item):
            typ = "/48"
            ret.append("set policy-options policy-statement " + PN + " term 2b from family inet6")
	    ret.append("set policy-options policy-statement " + PN + " term 2b from route-filter " + str(item) + " exact")
        else:
    	    typ = "/24"
            ret.append("set policy-options policy-statement " + PN + " term 2a from route-filter " + str(item) + " upto " + str(typ))
    ret.append("set policy-options policy-statement " + PN + " term 2a then next policy")
    ret.append("set policy-options policy-statement " + PN + " then reject")

    ret.append("edit policy-options policy-statement " + PN)
    ret.append('annotate term 1a "IPv4 blackhole"')
    if check:
        ret.append('annotate term 1b "IPv6 blackhole"')
    ret.append('annotate term 2a "customer IPv4 prefixes"')
    if check:
        ret.append('annotate term 2b "customer IPv6 prefixes"')

    return ret

def juniper_no_bh(pset,pname):
    ret = []
    ret.append("delete policy-options policy-statement " + str(pname))
    typ = "/24"
    check = 0
    for item in pset:
 	if re.match("^.*\:.*", item):            
            if check == 0:
                ret.append("set policy-options policy-statement " + str(pname) + " term 2b from family inet6")
	    typ = "/32"	 
            check = 1
            ret.append("set policy-options policy-statement " + str(pname) + " term 2b from route-filter " + str(item) + " exact")
        else:
            typ = "/24"
	    ret.append("set policy-options policy-statement " + str(pname) + " term 2a from route-filter " + str(item) + " upto " + str(typ))

    ret.append("set policy-options policy-statement " + str(pname) + " term 2a then next policy")
    ret.append("set policy-options policy-statement " + str(pname) + " then reject")

    ret.append("edit policy-options policy-statement " + str(pname))
    ret.append('annotate term 2a "customer IPv4 prefixes"')

    if check:
        ret.append('annotate term 2b "customer IPv6 prefixes"')

    return ret

def asset_obj_ripe(obj):
    x = []
    croot = "/usr/bin/whois -h whois.ripe.net "
    wt = croot + str(obj)
    p = subprocess.Popen(wt, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    d =[]

    retval = p.wait()

    for line in p.stdout.readlines():
        if re.match("^members:", line):
            line = re.sub("^members:\s+","",line)
            d = line.split(",")

    prefix = []
    asset = []

    for q in d:
      if re.match("^AS\d+", q):
        asset.append(q.rstrip())
        ok46 = croot + "-i origin " + q
        pp46 = subprocess.Popen(ok46, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        arr = []

        retval = pp46.wait()

        for l in pp46.stdout.readlines():
            if re.match("^(route:|route6:)", l):
		l = re.sub("^(route:|route6:)\s+","",l)
                arr.append(l.rstrip().lstrip())

        prefix.extend(arr)
      else:
        t = asset_obj(q)
        prefix.append(t)

    return prefix
