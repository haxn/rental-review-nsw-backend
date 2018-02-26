import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from database import db_session
from models import UserModel
from sqlalchemy import and_
import json
import jwt
import datetime

try:
    import config
    SECRET_SALT = config.SECRET_SALT
except Exception as e:
    SECRET_SALT = os.environ['SECRET_SALT']

class Users(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )

# Used to Create New User
class createUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()
        fbId = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(Users)
    encodedJwt = graphene.String()

    @staticmethod
    def mutate(root, info, **args):
        user_info = {
            'name': args.get('name'),
            'email': args.get('email'),
            'fbId': args.get('fbId')
        }

        user = UserModel(**user_info)

        db_session.add(user)
        db_session.commit()

        ok = True

        encoded_jwt = jwt.encode(
            {
                **user_info,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=90)
            },
            SECRET_SALT, algorithm='HS256'
        )

        return createUser(user=user, ok=ok, encodedJwt=encoded_jwt)

# # Used to Change Username with Email
# class changeUsername(graphene.Mutation):
#     class Arguments:
#         username = graphene.String()
#         email = graphene.String()
#
#     ok = graphene.Boolean()
#     user = graphene.Field(Users)
#
#     @staticmethod
#     def mutate(root, info, **args):
#         query = Users.get_query(context)
#         email = args.get('email')
#         username = args.get('username')
#         user = query.filter(UserModel.email == email).first()
#         user.username = username
#         db_session.commit()
#         ok = True
#
#         return changeUsername(user=user, ok = ok)

class refreshAuthToken(graphene.Mutation):
    class Arguments:
        auth_token = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(Users)

    @staticmethod
    def mutate(root, info, **args):
        query = Users.get_query(context)
        auth_token = args.get('auth_token')
        # username = args.get('username')
        # user = query.filter(UserModel.email == email).first()
        # user.username = username
        db_session.commit()
        ok = True

        return refreshAuthToken(user=user, ok = ok)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    user = SQLAlchemyConnectionField(Users)
    find_user = graphene.Field(lambda: Users, fbId = graphene.String())
    all_users = SQLAlchemyConnectionField(Users)

    def resolve_find_user(self, info, fbId):
        query = Users.get_query(info)
        # username = args.get('username')
        # you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
        return query.filter(UserModel.fbId == fbId).first()


class MyMutations(graphene.ObjectType):
    create_user = createUser.Field()
    # change_username = changeUsername.Field()

schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Users])

introspection_dict = schema.introspect()
schema_dict = {'data': introspection_dict}

# Print the schema in the console
# print (json.dumps(schema_dict))

# Or save the schema into some file
with open('schema.json', 'w') as fp:
    json.dump(schema_dict, fp)
