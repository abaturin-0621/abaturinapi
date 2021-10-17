from flask_restx import Namespace, Resource, fields
from flask import jsonify ,request ,abort,make_response
from src import api,db, bcrypt
from models.models import Item,User

api = Namespace('Items',path='/',description="Items managment")

item_shema = api.model(
    'item_shema',
        {
        'token': fields.String(required=True, description='The token'),
        'name': fields.String(required=True, description='The name item',min_length=2,max_length=20),
        }
    )

items_shema = api.model(
    'items_shema',
        {
        'token': fields.String(required=True, description='The token'),
        }
    )

item_new_shema_response_201= api.model(
    'items_new_shema_response_201',
        {
        "message": fields.String(default="Item created",required=True),
        "id": fields.Integer(required=True),
        "token": fields.String(required=True)
        }
    )     

item_delete_shema_response_200= api.model(
    'item_delete_shema_response_200',
        {
        "message": fields.String(default="Item delete",required=True),
        
        }
    )     

item_shema_response_200 = api.model("item_shema_response_200", {
    'id': fields.Integer(required=True, description='The items id'),
    'name': fields.String(required=True, description='The items name')
})

items_shema_response_200 = api.model("items_shema_response_200", {
    'result': fields.List(fields.Nested(item_shema_response_200)),
    
})




item_send_shema = api.model(
    'item_send_shema',
        {
        'token': fields.String(required=True, description='The token'),
        'username': fields.String(required=True, description='The username receiver'),
        'id': fields.Integer(required=True, description='The item id'),
        }
    )


item_send_shema_response_200 = api.model(
    'item_send_shema_response_200',
        {
        'link': fields.String(required=True, description='The link'),
        
        }
    )



@api.route("/items/new",methods = ["POST"])
@api.route("/items/<int:id>",methods =["DELETE"])
@api.route("/items",methods =["GET"])
class ItemClass(Resource):
    @api.doc(description='Create  item by name item and token user')
    @api.expect(item_shema,validate=True)
    @api.response(code=201, description="Success",model=item_new_shema_response_201)
    def post(self):
        token = request.json.get("token")
        name  = request.json.get("name")   
        user=User.decode_auth_token(token)
        if not user:
            abort(401, "Invalid token")
        try:
            item = Item(name=name,user_id=user.id)
            db.session.add(item)
            db.session.commit()
        except Exception:
            abort(500, "Internal Server Error")    
        response={'message':'Item created',
              "id":item.id,
              "token":token
              }    
        return make_response(jsonify(response), 201)


    @api.doc(description='Delete  item by  item id  and token user')
    @api.expect(items_shema,validate=True)
    @api.response(code=200, description="Success",model=item_delete_shema_response_200)
    def delete(self,id):
        token=request.json.get("token")
        user=User.decode_auth_token(token)
        if not user:
            abort(401, "Invalid token")

        item=Item.query.filter_by(id = id).first()
        if not item:
            abort(404, "No found item")
        try:
            db.session.delete(item)
            db.session.commit()  
        except Exception:
            abort(500, "Internal Server Error")         

        response={'message':" Item delete "}      
        return make_response(jsonify(response), 200)

    @api.doc(description='Get items by token user')
    @api.expect(items_shema,validate=True)
    @api.response(code=200, description="Success",model=items_shema_response_200)
    def get(self):
        token=(request.json.get('token'))
    
        user=User.decode_auth_token(token)
        if not user:
            abort(401, "Invalid token")
        
        items=Item.query.filter_by(user_id=user.id) 
        list_items=[{"id":item.id,"name":item.name} for item in items]

        response={'result':list_items}
        return make_response(jsonify(response), 200 )     

@api.route("/send",methods = ["POST"])
@api.route("/get",methods =["GET"])
class ItemOperationsClass(Resource):
    @api.doc(description='Generating a link to get an items')
    @api.expect(item_send_shema,validate=True)
    @api.response(code=200, description="Success",model=item_send_shema_response_200)
    def post(self):
        id = request.json.get("id")
        token_sender=request.json.get("token")
        username=request.json.get("username")
        user_sender=User.decode_auth_token(token_sender)
        if not user_sender:
            abort(401, "Invalid token")
        
        item=Item.query.filter_by(id=id ,user_id=user_sender.id).first()
        if not item:
            abort(404, "Item not found")

        user_receiver = User.query.filter_by(username = username).first() 
        if not user_receiver:
            abort(404, "User receiver not found")

        if user_receiver.id==user_sender.id:
            abort(409, "The object is already owned by the user")
        
        try: 
            token_receiver=user_receiver.encode_auth_token()
        except Exception:
            abort(500, "Internal Server Error")     

        link=f"{request.host_url}get?id={id}&token={token_receiver}"
        response={
            'link':link,
        }
        
        return make_response(jsonify(response), 200)

  

    @api.doc(description='Item rebinding')
    @api.doc(params={
        'id': {'description': 'The item id  for  rebinding',"required":"True"},
        'token': {'description': 'The token user receiver', 'in': 'query', 'type': 'string',"required":"True"}
            } 
        )
   
   
    def get(self):
        id = request.args.get("id")
        token=request.args.get('token')

        if not id:
            abort(400, "Bad request")

        if not token:
            abort(400, "Bad request")    

        user=User.decode_auth_token(token)
        if not user:
            abort(401, "Invalid token")
        
        item=Item.query.filter_by(id=id,user_id=user.id).first()
        if  item:
            abort(409, "The object is already owned by the user")

        item=Item.query.filter_by(id=id).first()
        if not item:
            abort(404, "Item no found")    

        try:
            item.user_id=user.id
            db.session.add(item)
            db.session.commit() 
        except Exception:
            abort(500, "Internal Server Error")         
        
        response={'result':'Item is bound to the user'
        }
        return make_response(jsonify(response), 200)    
