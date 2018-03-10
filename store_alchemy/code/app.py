from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)

# Set database type and access
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

"""
Turn off Flask SQLAlchemy mod tracker
Underlying SQLAlchemy mod tracker is still enabled and works better
"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'jose'
api = Api(app)

""" 
Before first request is made to the api, 
create tables if they do not already exist
"""
@app.before_first_request
def create_tables():
    db.create_all()

""" 
Create /auth endpoint
Use authenticate function to generate JWToken
Pass JWToken to identity function to authenticate user before relevant requests
"""
jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/item/<name>
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items') # http://127.0.0.1/items
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register') # http://127.0.0.1/register


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)