from flask import Flask, render_template, request
from flask_graphql import GraphQLView
from database import db_session
from schema import schema
from flask_cors import CORS

try:
    import config
except Exception as e:
    print(e)

app = Flask(__name__)
CORS(app)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql', schema=schema, graphiql=True, context={'session': db_session}
))

@app.route('/')
def index():
    return "Go to /graphql"

# @app.before_request
# def before_request():
    # print('Data: %s', request.data)
    # print('Body: %s', request.get_data())
    # print('Query string: %s', request.query_string)

# @app.after_request
# def after(response):
#   # todo with response
#   print (response.status)
#   return response


if __name__ == "__main__":
    # app.run()
    # try:
    #     app.run(host='0.0.0.0', debug=True, ssl_context=(config.SSL_CERT, config.SSL_KEY))
    # except:
    app.run(host='0.0.0.0', debug=True)
