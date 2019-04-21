import sys, textwrap

# Put your content here
HEX_CONTENT = (
"please replace me"
)

if len(sys.argv) != 2:
  print "usage: bin2hex.py <output filename>"
  sys.exit()


outfile = open(sys.argv[1],'wb')
outfile.write(HEX_CONTENT)
outfile.close()



