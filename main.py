import requests
import json
import os
import re
import data
import random
import time

base = os.path.dirname(os.path.abspath(__file__)) + '/'
with open(base + 'acc.txt') as f:
    acc = f.read().strip()
headers = {'Authorization':'Bearer ' + acc}
instance = 'https://twingyeo.kr'

def toot(message, toot_id):
    global toot_type
    d = dict()
    d['status'] = message
    d['visibility'] = toot_type
    d['in_reply'] = toot_id
    requests.post(instance + '/api/v1/statuses', headers = headers, data = d)

def follow(n):
    requests.post(instance + '/api/v1/accounts/' + str(n) + '/follow', headers = headers)

uri = instance + '/api/v1/streaming/user'
timeline = requests.get(uri, headers = headers, stream = True)
for t in timeline.iter_lines():
    dec = t.decode('utf-8')
    if dec == 'event: notification':
        newdec = json.loads(re.sub('data: ', '', dec))
        if newdec['type'] == 'mention':
            if newdec['account']['bot'] == False:
                msg = random.choice(data.kotoba)
                toot_id = newdec['status']['id']
                reply_to_account = newdec['account']['acct']
                message = '@' + reply_to_account + ' ' + msg
                toot_type = newdec['status']['visibility']
                if toot_type == 'public':
                    toot_type = 'unlisted'
                toot(message, toot_id)
            else:
                pass
        elif newdec['type'] == 'follow':
            n = newdec['account']['id']
            follow(n)