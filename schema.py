import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from database import db_session
from models import UserModel, ReviewModel, AgentModel, AgencyModel, PropertyModel, AgentRatingModel
from sqlalchemy import and_, exc
import json
import jwt
import datetime
from graphql import GraphQLError
import urllib.request
from helpers import from_global_id

try:
    import config
    SECRET_SALT = config.SECRET_SALT
except Exception as e:
    SECRET_SALT = os.environ['SECRET_SALT']


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class Review(SQLAlchemyObjectType):
    class Meta:
        model = ReviewModel
        interfaces = (relay.Node, )


class Agent(SQLAlchemyObjectType):
    class Meta:
        model = AgentModel
        interfaces = (relay.Node, )


class Property(SQLAlchemyObjectType):
    class Meta:
        model = PropertyModel
        interfaces = (relay.Node, )


class Agency(SQLAlchemyObjectType):
    class Meta:
        model = AgencyModel
        interfaces = (relay.Node, )


class UserInput(graphene.InputObjectType):
    fbId = graphene.String()
    fbAccessToken = graphene.String()


class BaseConnectionField(SQLAlchemyConnectionField):
    RELAY_ARGS = ['first', 'last', 'before', 'after']

    @classmethod
    def get_query(cls, model, info, **args):
        query = super(BaseConnectionField, cls).get_query(
            model, info, **args)
        for field, value in args.items():
            if field not in cls.RELAY_ARGS:
                query = query.filter(getattr(model, field) == value)
        return query

# class Query(graphene.ObjectType):
#     node = graphene.relay.Node.Field()
#     all_somethings = MyConnectionField(SomethingNode, field_name=grahene.String())


class PropertyInput(graphene.InputObjectType):
    addressString = graphene.String()
    lat = graphene.Float()
    lng = graphene.Float()
    googlePlacesId = graphene.String()
    currentAgent = graphene.String()
    currentAgency = graphene.String()


class ReviewInput(graphene.InputObjectType):
    property = graphene.Argument(PropertyInput)
    startDate = graphene.types.datetime.Date()
    endDate = graphene.types.datetime.Date()
    agent = graphene.String()
    agencyName = graphene.String()
    agencyCountry = graphene.String()
    agentRating = graphene.Float()
    weeklyRent = graphene.Float()
    bond = graphene.Float()
    bondReturned = graphene.Boolean()
    propertyRating = graphene.Float()
    neighbourRating = graphene.Float()
    phoneReception = graphene.Float()
    comments = graphene.String()


class createReview(graphene.Mutation):
    class Arguments:
        reviewFormData = graphene.Argument(ReviewInput)
        encodedJwt = graphene.String()
        userId = graphene.String()

    ok = graphene.Boolean()
    errorMessage = graphene.String()

    @staticmethod
    def mutate(root, info, **args):
        try:
            encoded_jwt = args.get('encodedJwt')
            userId = from_global_id(args.get('userId'))
            # userId = args.get('userId')

            jwt_user_info = jwt.decode(
                encoded_jwt, SECRET_SALT, algorithm='HS256')
            query = User.get_query(info)

            user = query.get(userId)

            if (jwt_user_info['email'] != user.email):
                raise Exception('Invalid JWT')

            # resolve agency
            agency = None
            if args.get('reviewFormData')['agencyName']:
                agency_query = Agency.get_query(info)
                existing_agency = agency_query.filter(AgencyModel.name == args.get(
                    'reviewFormData')['agencyName']).one_or_none()
                if existing_agency:
                    agency = existing_agency
                else:
                    agency = AgencyModel(name=args.get('reviewFormData')[
                        'agencyName'], country=args.get('reviewFormData')['agencyCountry'])
                    db_session.add(agency)
                    db_session.flush()
            elif args.get('reviewFormData')['agent'] is not None:
                raise('Cant create an agent without an agency')

            # resolve agent
            agent = None
            if args.get('reviewFormData')['agent']:
                agent_query = Agent.get_query(info)
                existing_agent = agent_query.filter(
                    AgentModel.name == args.get('reviewFormData')['agent']).one_or_none()
                if existing_agent:
                    agent = existing_agent
                else:
                    print(agency.id)
                    agent = AgentModel(name=args.get('reviewFormData')[
                        'agent'], agencyId=agency.id)
                    db_session.add(agent)
                    db_session.flush()
                agentRating = AgentRatingModel(
                    agentId=agent.id, rating=args.get('reviewFormData')['agentRating'])
                db_session.add(agentRating)
                db_session.flush()

            # resolve property
            property = None
            property_query = Property.get_query(info)
            existing_property = property_query.filter(PropertyModel.googlePlacesId == args.get(
                'reviewFormData')['property']['googlePlacesId']).one_or_none()
            if existing_property is None:
                property_info = {
                    'addressString': args.get('reviewFormData')['property']['addressString'],
                    'lat': args.get('reviewFormData')['property']['lat'],
                    'lng': args.get('reviewFormData')['property']['lng'],
                    'googlePlacesId': args.get('reviewFormData')['property']['googlePlacesId'],
                    'currentAgent': agent.id,
                    'currentAgency': agency.id
                }
                property = PropertyModel(**property_info)
                db_session.add(property)
                db_session.flush()
            else:
                property = existing_property

            # resolve review
            review_info = {
                'propertyId': property.id,
                'userId': userId,
                'startDate': args.get('reviewFormData')['startDate'],
                'endDate': args.get('reviewFormData')['endDate'],
                'weeklyRent': args.get('reviewFormData')['weeklyRent'],
                'bond': args.get('reviewFormData')['bond'],
                'bondReturned': args.get('reviewFormData')['bondReturned'],
                'propertyRating': args.get('reviewFormData')['propertyRating'],
                'neighbourRating': args.get('reviewFormData')['neighbourRating'],
                'phoneReception': args.get('reviewFormData')['phoneReception'],
                'comments': args.get('reviewFormData')['phoneReception']
            }

            review = ReviewModel(**review_info)
            db_session.add(review)
            db_session.commit()

            ok = True
            errorMessage = None
        except Exception as e:
            print(e)
            ok = False
            errorMessage = str(e)
            db_session.rollback()

        return createReview(ok=ok, errorMessage=errorMessage)


# Used to Create New User
class createUser(graphene.Mutation):
    class Arguments:
        credentials = graphene.Argument(UserInput)

    ok = graphene.Boolean()
    user = graphene.Field(User)
    encodedJwt = graphene.String()

    @staticmethod
    def mutate(root, info, **args):
        try:
            credentials = args.get('credentials')
            api = 'https://graph.facebook.com/v2.3/{}?fields=name,email&access_token={}'.format(
                credentials.fbId, credentials.fbAccessToken)
            user_info_blob = urllib.request.urlopen(api).read()
            user_info_obj = json.loads(user_info_blob.decode("utf-8"))

            pic_data_link = 'https://graph.facebook.com/v2.3/{}/picture?width=500&redirect=false&access_token={}'.format(
                credentials.fbId, credentials.fbAccessToken)

            pic_data_blob = urllib.request.urlopen(pic_data_link).read()
            pic_url = json.loads(pic_data_blob.decode("utf-8"))['data']['url']

            user_info = {
                'name': user_info_obj['name'],
                'email': user_info_obj['email'],
                'fbId': user_info_obj['id'],
                'profilePicture': pic_url
            }
            user = UserModel(**user_info)

            # check for existing user
            query = User.get_query(info)
            existing_user = query.filter(
                UserModel.fbId == user_info['fbId']).one_or_none()

            if existing_user is None:
                user.createdDate = datetime.datetime.utcnow()
                db_session.add(user)
            else:
                user.createdDate = existing_user.createdDate
                existing_user.name = user_info['name']
                existing_user.email = user_info['email']
                existing_user.profilePicture = pic_url

                db_session.add(existing_user)

            db_session.commit()

            ok = True
            encoded_jwt = jwt.encode(
                {
                    **user_info,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=90)
                },
                SECRET_SALT, algorithm='HS256'
            ).decode('utf-8')

        except Exception as e:
            print(e)
            ok = False
            user = None
            encoded_jwt = None
            db_session.rollback()

        return createUser(user=user, ok=ok, encodedJwt=encoded_jwt)


# class getAuthToken(graphene.Mutation):
#     class Arguments:
#         fbId = graphene.String()
#
#     ok = graphene.Boolean()
#     encodedJwt = graphene.String()
#
#     @staticmethod
#     def mutate(root, info, **args):
#         try:
#             fb_id = args.get('fbId')
#             query = User.get_query(info)
#             user = query.filter(UserModel.fbId == fb_id).one()
#             user_info = {
#                 'name': user.name,
#                 'email': user.email,
#                 'fbId': fb_id
#             }
#
#             ok = True
#             encoded_jwt = jwt.encode(
#                 {
#                     **user_info,
#                     'exp': datetime.datetime.utcnow() + datetime.timedelta(days=90)
#                 },
#                 SECRET_SALT, algorithm='HS256'
#             ).decode('utf-8')
#
#         except Exception as e:
#             print(str(e))
#             ok = False
#             encoded_jwt = None
#         return getAuthToken(user=user, ok=ok, encodedJwt=encoded_jwt)


class refreshAuthToken(graphene.Mutation):
    class Arguments:
        encodedJwt = graphene.String()
        fbId = graphene.String()

    ok = graphene.Boolean()
    encodedJwt = graphene.String()
    user = graphene.Field(User)

    @staticmethod
    def mutate(root, info, **args):
        try:
            encoded_jwt = args.get('encodedJwt')
            fb_id = args.get('fbId')

            jwt_user_info = jwt.decode(
                encoded_jwt, SECRET_SALT, algorithm='HS256')
            query = User.get_query(info)

            user = query.filter(UserModel.fbId == fb_id).one()

            if (jwt_user_info['email'] != user.email):
                raise Exception(
                    'Attempting to refresh key belonging to other user')

            new_encoded_jwt = jwt.encode(
                {
                    **jwt_user_info,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=90)
                },
                SECRET_SALT, algorithm='HS256'
            ).decode('utf-8')

            ok = True

        except Exception as e:
            print(str(e))
            ok = False
            new_encoded_jwt = None
            user = None
            db_session.rollback()

        return refreshAuthToken(ok=ok, encodedJwt=new_encoded_jwt, user=user)

        # query = User.get_query(context)
        # auth_token = args.get('auth_token')
        # # username = args.get('username')
        # # user = query.filter(UserModel.email == email).one()
        # # user.username = username
        # db_session.commit()
        # ok = True
        #
        # return refreshAuthToken(user=user, ok = ok)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # user = SQLAlchemyConnectionField(User)
    # find_user = graphene.Field(User, fbId=graphene.String(), encodedJwt=graphene.String())
    # all_User = SQLAlchemyConnectionField(User)
    find_agencies = BaseConnectionField(
        Agency, countryName=graphene.String())
    all_agencies = BaseConnectionField(Agency)

    # def resolve_find_agencies(self, info, countryName):
    #     query = Agency.get_query(info)
    #     print('called find agency')
    #     agencies = query.filter(AgencyModel.country == countryName)
    #     print(agencies)
    #     return agencies

    # def resolve_find_user(self, info, fbId, encodedJwt):
    #     user_info = jwt.decode(encodedJwt, SECRET_SALT, algorithm='HS256')
    #     query = User.get_query(info)
    #     user = query.filter(UserModel.fbId == fbId).one()
    #
    #     # username = args.get('username')
    #     # you can also use and_ with filter() eg: filter(and_(param1, param2)).one()
    #     # return query.filter(UserModel.fbId == fbId).one()
    #     return None


class MyMutations(graphene.ObjectType):
    create_user = createUser.Field()
    refresh_auth_token = refreshAuthToken.Field()
    create_review = createReview.Field()
    # get_auth_token = getAuthToken.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations, types=[User])

introspection_dict = schema.introspect()
schema_dict = {'data': introspection_dict}

# Print the schema in the console
# print (json.dumps(schema_dict))

# Or save the schema into some file
with open('schema.json', 'w') as fp:
    json.dump(schema_dict, fp)
