from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec import FlaskApiSpec
from docs import register_docs
from api import restapi

DATABASE = '../database/canndb.db'



app = Flask(__name__)
CORS(app)


with app.app_context():
    app.register_blueprint(restapi,  url_prefix='/api')

register_docs(app)

if __name__ == '__main__':
    app.run(debug=True)