import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_restx import Api, Resource, fields
from flask_restx import Api
# from flask import jsonify,request,make_response
from werkzeug.exceptions import NotFound





app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'db','apidb.db'))
app.config["SECRET_KEY"] = '2688088b53e6e0116a1ddb59f72db9d1'
app.config["EXPIRE_TOKEN_SECOND"] = 6000
api = Api(
    app = app,
    title='User and items managment',
    version='1.0',
    description='User and items managment',
    doc='/swagger',
    catch_all_404s=True,
    prefix='/api'
    
    
    
)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from .items import api as items
from .users import api as users

api.add_namespace(users)
api.add_namespace(items)

@api.errorhandler(NotFound)
def handle_no_result_exception(error):
    '''Return a custom not found error message and 404 status code'''
    return {'message': "The requested url was not found on this server"}, 404
