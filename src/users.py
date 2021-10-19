from flask_restx import Namespace, Resource, fields
from flask import jsonify ,request ,abort,make_response
from src import api,db, bcrypt
from models.models import User

api = Namespace('Users',path="/",description="Users managment")
users_shema = api.model(
    'users',
        {
        'username': fields.String(required=True, description='The username',min_length=2,max_length=50),
        'password': fields.String(required=True, description='The password',min_length=2,max_length=50),
        }
    )
user_login_shema_response_200= api.model(
    'user_registation_response_200',
         {
            "message": fields.String(default="The user was autorised"),
            "token": fields.String(required=True, description='The token'),

        }    
    )

user_registration_shema_response_201= api.model(
    'user_registation_response_201',
        {
        "message": fields.String(default="The user was created")
        }
    )  

user_registration_shema_response_409= api.model(
    'user_registration_shema_response_409',
        {
        "message": fields.String(default="The user with such a login already exists")
        }
    )        

user_login_shema_response_401= api.model(
    'user_login_shema_response_401',
        {
        "message": fields.String(default="Unauthorized")
        }
    )       



@api.route("/registration")
class RegistrationClass(Resource):
    @api.doc(description='Registration user by username')
    @api.expect(users_shema,validate=True)
    @api.response(code=201, description="Success",model=user_registration_shema_response_201)
    @api.response(code=409, description="Error",model=user_registration_shema_response_409)
    def post(self):
        username = request.json.get("username")
        password  = request.json.get("password")   

        if User.query.filter_by(username = username).first():
            abort(409, "The user with such a login already exists")

        try:       
            hash_pass = bcrypt.generate_password_hash(password)     
            user= User(username = username, password = hash_pass)
            db.session.add(user)
            db.session.commit()
        except Exception:
            abort(500, "Internal Server Error")  
        response={ 
            "message": "The user was created"
        }
        
        return make_response(jsonify(response), 201)

@api.route("/login")
class LoginClass(Resource):
    @api.doc(description='Login user by username and password')
    @api.expect(users_shema,validate=True)
    @api.response(code=200, description="Success",model=user_login_shema_response_200)
    @api.response(code=401, description="Error",model=user_login_shema_response_401)
    def post(self):
        username = request.json.get("username")
        password  = request.json.get("password")   
        user = User.query.filter_by(username = username).first()
        if not (user and bcrypt.check_password_hash(user.password, password)):
           abort(401, "Wrong login or password")
        try: 
            token=user.encode_auth_token()
        except Exception:
            abort(500, "Internal Server Error")    
        response = {
            "message": "The user was autorised",
            "token":token,

        }    
        return make_response(jsonify(response), 200)

