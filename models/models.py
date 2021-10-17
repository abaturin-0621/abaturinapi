from src import db
from datetime import datetime as dt
import jwt
from src import app

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(40), nullable = False)

    
    def encode_auth_token(self):
        current_time=dt.timestamp(dt.now())
        token_data = {
                'time': current_time,
                'user_id': self.id
            }
        return jwt.encode(
                token_data,
                app.config.get('SECRET_KEY'),
                algorithm='HS256',
            ).decode("utf-8") 

    def decode_auth_token(token):
        current_time=dt.timestamp(dt.now())
        expire=app.config.get('EXPIRE_TOKEN_SECOND')

        try:
            token_data=jwt.decode(token,app.config.get('SECRET_KEY'),algorithm='HS256')
        except Exception:
            return False    

        user_id=token_data["user_id"]
        create_time=token_data["time"]

        if current_time-create_time>expire:
            return False  

        return User.query.filter_by(id = user_id).first()    
               

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique = False, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
