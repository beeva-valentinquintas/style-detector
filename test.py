import requests
import sys

filename = 'resources/hipster.jpg'

if len(sys.argv) == 3:
    filename = sys.argv[2]
else:
    print "Usage: test.py -f filename\n"
    sys.exit(0)
    
print "Filename is {}".format(filename)
data = open(filename, 'rb').read()

import base64
data64 = base64.b64encode(data)
res = requests.post(url='http://localhost:5000/labels',
                    data=data64,
                    headers={'Content-Type': 'application/octet-stream'})

print res.json()['myself']['styles']
