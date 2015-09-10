import sys
from id3.id3 import ID3


if len(sys.argv) != 2:
    sys.exit(0)

musicFile = sys.argv[1]
print "Reading ID3 Tags from %s" % musicFile

parser = ID3(musicFile)
