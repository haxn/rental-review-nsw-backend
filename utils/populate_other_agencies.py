from database import db_session
from models import UserModel, ReviewModel, AgentModel, AgencyModel, PropertyModel, AgentRatingModel
import json
db_session.rollback()
agencies = []
with open('utils/australian-postcodes.sql') as f:
    content = f.readlines()
    for line in content:
        line = line.strip()
        if line.startswith('('):
            suburb = ((line.split('\'')[3]).title())
            state = line.split('\'')[5]
            print(state)
            print(suburb)

            agencies.append(AgencyModel(
                name='Other',
                suburb=suburb,
                countryName='Australia',
                state=state,
            ))


for agency in agencies:
    print(agency)
    db_session.add(agency)
    db_session.flush()
db_session.commit()

# db_session.bulk_save_objects(agencies)
# print('bulk add done')
# db_session.commit()

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
