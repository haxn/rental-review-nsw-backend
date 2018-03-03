from flask import Flask, render_template
from flask_graphql import GraphQLView
from database import db_session
from schema import schema

try:
    import config
except Exception as e:
    print(e)

app = Flask(__name__)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql', schema=schema, graphiql=True, context={'session': db_session}
))

@app.route('/')
def index():
    return "Go to /graphql"


if __name__ == "__main__":
    app.run(host= '0.0.0.0')
