from database import db_session
from models import UserModel, ReviewModel, AgentModel, AgencyModel, PropertyModel, AgentRatingModel
import json
db_session.rollback()
agency_query = db_session.query(AgencyModel)
agent_query = db_session.query(AgentModel)

agents = []
with open('backup_data/agents.json') as all_agents_file:
    lines = all_agents_file.readlines()
    for index, line in enumerate(lines):
        agent = json.loads(line)
        # try:
        agency = agency_query.filter(
            AgencyModel.name == agent['agentAgencyName']).one_or_none()
        if agency is None:
            try:
                agency = agency_query.filter(AgencyModel.name == 'Other').filter(
                    AgencyModel.suburb == agent['suburb'].title()).one()
            except:
                agencies = agency_query.filter(AgencyModel.name == 'Other').filter(
                    AgencyModel.suburb == agent['suburb'].title()).all()
                print('Suburb: %s, Count: %s' %
                      (agent['suburb'].title(), len(agencies)))

                for agency in agencies[1:]:
                    db_session.delete(agency)
                    db_session.flush()
                agency = agencies[0]
        db_session.commit()

        # print(agency.name)
        # except:
        #     print('agent: %s has more than one entry.' %
        #           agent['agentAgencyName'])
        #     agencies = agency_query.filter(
        #         AgencyModel.name == agent['agentAgencyName']).all()
        #     for agency in agencies:
        #         print(agency.suburb)
        #     break

        # if len(agencies) > 1:
        #     for agency in agencies[1:]
        #         db_session.delete(agency)
        #         db_session.flush()

        existing_agent = agent_query.filter(
            AgentModel.domainId == agent.get('domainId', None)).one_or_none()

        if existing_agent is None:
            existing_agent = AgentModel(
                name=agent.get('cardTitle', None),
                agentAvatarUrl=agent.get('agentAvatarUrl', None),
                brandColour=agent.get('brandColour', None),
                emailAddress=agent.get('emailAddress', None),
                phoneNumber=agent.get('phoneNumber', None),
                domainProfileUrl=agent.get('domainProfileUrl', None),
                domainId=agent.get('domainId', None),
            )
            agents.append(existing_agent)
        agency.agentIds.append(existing_agent)
        db_session.add(agency)
        db_session.flush()
        print('Added agent: %s' % agent.get('cardTitle', None))
        print(index/len(lines)*100)


for index, agent in enumerate(agents):
    print('Adding agency')
    print(index/len(agents)*100)
    db_session.add(agent)
    db_session.flush()
db_session.commit()
