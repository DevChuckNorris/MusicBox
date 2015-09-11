import sys
from id3.id3 import ID3


if len(sys.argv) != 2:
    sys.exit(0)

musicFile = sys.argv[1]

parser = ID3(musicFile)

print 'Title: %s, Artist: %s, Album: %s' % \
      (parser.get_frame('TIT2'), parser.get_frame('TPE2'), parser.get_frame('TALB'))

if parser.contains_frame('PRIV'):
    print bytearray(parser.get_frame('PRIV')).decode('UTF8')
