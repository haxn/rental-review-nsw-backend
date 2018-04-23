import requests
from string import ascii_lowercase
import time
import json


resp = requests.post('https://auth.domain.com.au/v1/connect/token',
                     auth=('eqkj6bcysx8rpguzs7p52v2k',
                           'hnV6DurmhV'),
                     headers={
                         'content-type': 'application/x-www-form-urlencoded'
                     },
                     data={
                         'grant_type': 'client_credentials',
                         'scope': 'api_agencies_read'
                     })
print(resp.text)
auth_token = resp.json()['access_token']


agent_list = []

suburbs = []
# with open('utils/australian-postcodes.sql') as f:
#     content = f.readlines()
#     for line in content:
#         line = line.strip()
#         if line.startswith('('):
#             suburbs.append(line.split('\'')[3])

# suburbs = '-'.join(list(set(suburbs)))

# for suburb in suburbs:
# print(suburbs)
page = 1
while True:
    print('page: %s' % (page))
    resp = requests.get('https://api.domain.com.au/v1/agents/search',
                        headers={
                            'Authorization': 'Bearer ' + auth_token,
                            'Content-Type': 'application/json'
                        },
                        params={
                            'query': 'a',
                            'pageNumber': page,
                            'pageSize': 100

                        })

    if resp.status_code == 200:
        results = resp.json()

        for result in results:
            agent_list.append(result)
    else:
        print(resp.text)

    if len(results) != 100:
        break
    else:
        page = page + 1

    time.sleep(0.5)

seen_agencies = []
set_of_agencies = []

for agent in agent_list:
    agent['name'] = agent['name'].strip()
    if agent['name'] in seen_agencies:
        continue
    else:
        set_of_agencies.append(agent)
        seen_agencies.append(agent['name'])

sorted_agencies = sorted(set_of_agencies, key=lambda i: i['name'])

with open('utils/agents_a.json', 'w') as outfile:
    json.dump(sorted_agencies, outfile)

for agent in sorted_agencies:
    print(agent['name'])
