# small python script to dump a binary file to an array of hex bytes
# corelanc0d3r - www.corelan-consulting.com


import sys, textwrap

if len(sys.argv) != 2:
  print "usage: bin2hex.py <file>"
  sys.exit()

  
print "Reading %s" % sys.argv[1]
infile = open(sys.argv[1],'rb')
content = infile.read()
infile.close()

nullsCount = 0

out = ""
totalbytes = 0
for c in content:
  byte = ord(c)
  out += "\\x%02x" % byte
  totalbytes += 1
  if byte == 0:
    nullsCount += 1

print "Read %d bytes" % totalbytes
	
print """
--------------------------------------------
Displaying bytes as hex :
--------------------------------------------
"""

for line in textwrap.wrap(out, 32):
  print "\"%s\"" % line
  
print "\nNumber of nulls : %d" % nullsCount


print """\n
--------------------------------------------
Displaying bytes as ascii :
--------------------------------------------
"""

for line in textwrap.wrap(content,50):
  print line