import requests
import json
import os
import re
import data
import random

base = os.path.dirname(os.path.abspath(__file__))+'/'
with open(base+'acc.txt') as f:
    acc = f.read().strip()
headers = {'Authorization':'Bearer '+acc}
instance = 'instance_name'

def toot(message, toot_id):
    d = dict()
    d['status'] = message
    d['visibility'] = 'unlisted'
    d['in_reply_to_id'] = toot_id
    r = requests.post(instance+'/api/v1/statuses', headers=headers, data=d)

uri = instance+'/api/v1/streaming/user'
timeline = requests.get(uri, headers=headers, stream=True)
for t in timeline.iter_lines():
    dec = t.decode('utf-8')
    if dec == 'event: update':
        stat = 1
    elif dec == ':)':
        stat = 1
    elif dec == 'event: notification':
        stat = 0
    elif dec == ':thump':
        stat = 1
    if stat:
        pass
    else:
        try:
            newdec = json.loads(re.sub('data: ','',dec))
            if newdec['type'] == 'mention':
                print("new mention")
                msg = random.choice(data.kotoba)
                print('message: '+msg)
                toot_id = newdec['status']['id']
                print('toot_id: '+str(toot_id))
                reply_to_account = newdec['account']['acct']
                print('reply_to_account: '+reply_to_account)
                message = '@'+reply_to_account+' '+msg
                print('--------------------------------------------------')
                toot(message, toot_id)
        except:
            pass