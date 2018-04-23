import requests
from string import ascii_lowercase
import time
import json
from lxml import html
import re


def extract(s):
    start = s.find('"results":[')
    if start == -1:
        # No opening bracket found. Should this be an error?
        raise Exception('error')
    start += 1  # skip the bracket, move to the next character
    end = s.find(']', start)
    if end == -1:
        raise Exception('error')
    else:
        temp = s[start:end]
        temp_2 = temp[9:]
        temp_3 = temp_2+']'
        # print(temp_3)
        return json.loads(temp_3)


entries = []
with open('utils/australian-postcodes.sql') as f:
    content = f.readlines()
    for line in content:
        line = line.strip()
        if line.startswith('('):
            suburb = ((line.split('\'')[3]).replace(' ', '-'))
            postcode = line.split('\'')[1]
            state = line.split('\'')[5]
            search_key = '-'.join([suburb, state, postcode])
            info = (search_key, line.split('\'')[
                    3].capitalize(), line.split('\'')[5])
            entries.append(info)
page = 1
with open('utils/agents_c.json', 'w') as outfile:
    for index, entry in enumerate(entries[10000:15000]):
        (search_key, suburb, state) = entry
        print(search_key)
        print(suburb)
        print(state)
        print('%f percent complete' % ((index/10000)*100))
        while True:
            resp = requests.get(
                'https://www.domain.com.au/real-estate-agents/{}/?agentFilter=property-managers&page={}'.format(search_key, page))
            try:
                data = extract(resp.text)
                # print('got %s entries' % len(data))
                for agent in data:
                    agent['state'] = state
                    agent['suburb'] = suburb
                    print('writing data')
                    print(json.dumps(agent), file=outfile)
                    # outfile.writelines(json.dumps(agent))
                    # json.dump(agent, outfile)
                if len(data) == 18:
                    page += 1
                else:
                    raise Exception('no next page')
            except Exception as e:
                print(e)
                page = 1
                outfile.flush()
                break
