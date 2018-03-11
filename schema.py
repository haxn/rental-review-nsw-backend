import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from database import db_session
from models import UserModel
from sqlalchemy import and_
import json
import jwt
import datetime
from graphql import GraphQLError
import urllib.request

try:
    import config
    SECRET_SALT = config.SECRET_SALT
except Exception as e:
    SECRET_SALT = os.environ['SECRET_SALT']


class Users(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )

class UserInput(graphene.InputObjectType):
    fbId = graphene.String()
    fbAccessToken = graphene.String()

# Used to Create New User
class createUser(graphene.Mutation):
    class Arguments:
        credentials = graphene.Argument(UserInput)

    ok = graphene.Boolean()
    user = graphene.Field(Users)
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
            print(pic_url)

            user_info = {
                'name': user_info_obj['name'],
                'email': user_info_obj['email'],
                'fbId': user_info_obj['id'],
                'profilePicture': pic_url
            }
            user = UserModel(**user_info)


            ## check for existing user
            query = Users.get_query(info)
            existing_user = query.filter(UserModel.fbId == user_info['fbId']).first()

            if existing_user is None:
                db_session.add(user)
            else:
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
#             query = Users.get_query(info)
#             user = query.filter(UserModel.fbId == fb_id).first()
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
    user = graphene.Field(Users)

    @staticmethod
    def mutate(root, info, **args):
        try:
            encoded_jwt = args.get('encodedJwt')
            fb_id = args.get('fbId')

            jwt_user_info = jwt.decode(encoded_jwt, SECRET_SALT, algorithm='HS256')
            query = Users.get_query(info)

            user = query.filter(UserModel.fbId == fb_id).first()

            if (jwt_user_info['email'] != user.email):
                raise Exception('Attempting to refresh key belonging to other user')


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


        return refreshAuthToken(ok=ok, encodedJwt=new_encoded_jwt, user=user)

        # query = Users.get_query(context)
        # auth_token = args.get('auth_token')
        # # username = args.get('username')
        # # user = query.filter(UserModel.email == email).first()
        # # user.username = username
        # db_session.commit()
        # ok = True
        #
        # return refreshAuthToken(user=user, ok = ok)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    user = SQLAlchemyConnectionField(Users)
    find_user = graphene.Field(lambda: Users, fbId=graphene.String(), encodedJwt=graphene.String())
    all_users = SQLAlchemyConnectionField(Users)

    def resolve_find_user(self, info, fbId, encodedJwt):
        user_info = jwt.decode(encodedJwt, SECRET_SALT, algorithm='HS256')
        query = Users.get_query(info)
        user = query.filter(UserModel.fbId == fbId).first()
        print(user_info)
        print(user)

        # username = args.get('username')
        # you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
        # return query.filter(UserModel.fbId == fbId).first()
        return None


class MyMutations(graphene.ObjectType):
    create_user = createUser.Field()
    refresh_auth_token = refreshAuthToken.Field()
    # get_auth_token = getAuthToken.Field()

schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Users])

introspection_dict = schema.introspect()
schema_dict = {'data': introspection_dict}

# Print the schema in the console
# print (json.dumps(schema_dict))

# Or save the schema into some file
with open('schema.json', 'w') as fp:
    json.dump(schema_dict, fp)
