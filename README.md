# irrtool
toolkit help to create prefixes configs on cisco_xr and juniper routers depends on whois.ripe.net 

you can use this command line tool eg.

bash# python get_prefixes.py AS-2K YOUR-ROUTER-POLICY-NAME junos|cisco_xr Y|N

In ourput depends on command line switches you will get ready to paset config for chosen router type.

eg.

root@mm:/home/mm/irrmoth# python get_prefixes.py AS-2K test-policy cisco_xr Y

----------><----------><------------><-----------><----------><------------><-----------

prefix-set test-policy<br>
  86.105.244.0/22 ge 32,<br>
  86.105.245.0/24 ge 32,<br>
  89.45.176.0/20 ge 32,<br>
  89.47.56.0/23 ge 32,<br>
  2001:67c:490::/48 ge 128,<br>
  195.138.192.0/24 ge 32,<br>
  81.180.200.0/24 ge 32,<br>
  193.227.110.0/24 ge 32,<br>
  193.26.129.0/24 ge 32,<br>
  194.102.96.0/24 ge 32,<br>
  94.176.180.0/23 ge 32,<br>
  94.176.180.0/24 ge 32,<br>
  94.176.181.0/24 ge 32,<br>
  91.216.157.0/24 ge 32,<br>
  195.216.218.0/24 ge 32,<br>
  195.28.162.0/23 ge 32,<br>
  85.120.232.0/23 ge 32,<br>
  176.126.198.0/23 ge 32,<br>
  176.126.198.0/24 ge 32,<br>
  176.126.199.0/24 ge 32,<br>
  176.126.206.0/23 ge 32,<br>
  176.126.206.0/24 ge 32,<br>
  176.126.207.0/24 ge 32<br>
end-set<br>

----------><----------><------------><-----------><----------><------------><-----------
