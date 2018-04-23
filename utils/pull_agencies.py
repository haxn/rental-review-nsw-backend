import requests
from string import ascii_lowercase
import time
import json


resp = requests.post('https://auth.domain.com.au/v1/connect/token',
                     auth=('93vc4hgvhd9y4zrhhkxjrqnz',
                           'DdhEHbCyrR'),
                     headers={
                         'content-type': 'application/x-www-form-urlencoded'
                     },
                     data={
                         'grant_type': 'client_credentials',
                         'scope': 'api_agencies_read'
                     })
print(resp.text)
auth_token = resp.json()['access_token']


agency_list = []

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
for c in 'aeiou':
    page = 1
    while True:
        print('letter: %s, page: %s' % (c, page))
        resp = requests.get('https://api.domain.com.au/v1/agencies',
                            headers={
                                'Authorization': 'Bearer ' + auth_token,
                                'Content-Type': 'application/json'
                            },
                            params={
                                'q': c,
                                'pageNumber': page,
                                'pageSize': 100

                            })

        if resp.status_code == 200:
            results = resp.json()

            for result in results:
                agency_list.append(result)
        else:
            print(resp.text)

        if len(results) != 100:
            break
        else:
            page = page + 1

        time.sleep(0.5)

seen_agencies = []
set_of_agencies = []

for agency in agency_list:
    agency['name'] = agency['name'].strip()
    if agency['name'] in seen_agencies:
        continue
    else:
        set_of_agencies.append(agency)
        seen_agencies.append(agency['name'])

sorted_agencies = sorted(set_of_agencies, key=lambda i: i['name'])

with open('utils/agencies.json', 'w') as outfile:
    json.dump(sorted_agencies, outfile)

for agency in sorted_agencies:
    print(agency['name'])
