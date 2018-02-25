import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from database import db_session
from models import UserModel
from sqlalchemy import and_
import json


class Users(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )

# Used to Create New User
class createUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(Users)

    @staticmethod
    def mutate(root, info, **args):
        user = UserModel(name=args.get('name'), email=args.get('email'))
        db_session.add(user)
        db_session.commit()
        ok = True
        return createUser(user=user, ok=ok)

# Used to Change Username with Email
class changeUsername(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(Users)

    @staticmethod
    def mutate(root, info, **args):
        query = Users.get_query(context)
        email = args.get('email')
        username = args.get('username')
        user = query.filter(UserModel.email == email).first()
        user.username = username
        db_session.commit()
        ok = True

        return changeUsername(user=user, ok = ok)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    user = SQLAlchemyConnectionField(Users)
    find_user = graphene.Field(lambda: Users, name = graphene.String())
    all_users = SQLAlchemyConnectionField(Users)

    def resolve_find_user(self, info, name):
        query = Users.get_query(info)
        # username = args.get('username')
        # you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
        return query.filter(UserModel.name == name).first()


class MyMutations(graphene.ObjectType):
    create_user = createUser.Field()
    change_username = changeUsername.Field()

schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Users])

introspection_dict = schema.introspect()

# Print the schema in the console
print (json.dumps(introspection_dict))

# Or save the schema into some file
with open('schema.json', 'w') as fp:
    json.dump(introspection_dict, fp)
