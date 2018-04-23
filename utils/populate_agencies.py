from database import db_session
from models import UserModel, ReviewModel, AgentModel, AgencyModel, PropertyModel, AgentRatingModel
import json
db_session.rollback()
tmp_agency_url = {}
with open('backup_data/agents.json') as all_agents_file:
    lines = all_agents_file.readlines()
    for line in lines:
        agent = json.loads(line)
        tmp_agency_url[agent['agentAgencyName']] = agent['agencyLogoUrl']

all_agencies_json = json.load(open('backup_data/agencies.json'))

agencies = []
for agency in all_agencies_json:
    # agencies[agency['name']] = agency
    try:
        logo = tmp_agency_url[agency['name']]
    except:
        logo = None

    agencies.append(AgencyModel(
        name=agency.get('name', None),
        suburb=agency.get('suburb', None),
        countryName='Australia',
        address1=agency.get('address1', None),
        address2=agency.get('address2', None),
        telephone=agency.get('telephone', None),
        rentalTelephone=agency.get('rentalTelephone', None),
        mobile=agency.get('mobile', None),
        fax=agency.get('fax', None),
        state=agency.get('state', None),
        description=agency.get('description', None),
        email=agency.get('email', None),
        rentalEmail=agency.get('rentalEmail', None),
        numberForRent=agency.get('numberForRent', None),
        domainUrl=agency.get('domainUrl', None),
        agencyLogoUrl=tmp_agency_url.get(agency['name'], None),
        domainId=agency.get('id', None)
    ))


for agency in agencies:
    print(agency)
    db_session.add(agency)
    db_session.flush()
    db_session.commit()


#     print(all_agencies_json['inSuburb'])
#     for key in agency.keys():
#         if key not in agency_keys:
#             agency_keys.append(key)

# print(agency_keys)

# agent_keys = []
# with open('backup_data/agents.json') as all_agents_file:
#     lines = all_agents_file.readlines()
#     for line in lines:
#         agent = json.loads(line)
#         if agent['agentAgencyName'] in agencies.keys():
#             print('found')
#         else:
#             print('not found')
#         # for key in agent.keys():
#         #     if key not in agent_keys:
#         #         agent_keys.append(key)
