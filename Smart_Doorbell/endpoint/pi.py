from json import encoder
import socket
import os
import urllib.request
import json
import base64

def post_img(path, mode = 'Error'):
    f = open(os.path.join('./usr', path), 'rb')
    encoder = str(base64.b64encode(f.read()), 'utf-8')
    msg1 = {'image': encoder,
              'mode': mode,
            }
    jmsg1 = json.dumps(msg1)
    print(jmsg1)
    urllib.request.urlopen(f'http://140.112.18.2:11064/{str(jmsg1).replace(" ","%20")}')

post_img('test.jpg')