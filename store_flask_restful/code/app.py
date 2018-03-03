from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'password'
api = Api(app)

""" 
Create /auth endpoint
Use authenticate function to generate JWToken
Pass JWToken to identity function to authenticate user before relevant requests
"""
jwt = JWT(app, authenticate, identity) # /auth

items = []

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    @jwt_required()
    def get(self, name):
        """ Takes an item name and returns the item """
        item = next((item for item in items if item['name'] == name), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        """ 
        Takes an item name and json data and adds it to stored items
        Returns the item if accepted, returns 400 and error if already exists
        """
        if next((item for item in items if item['name'] == name), None):
            return {"Message": "An item with name {} already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        """
        Delete an item from the list of items
        Return message if successful
        """
        global items
        items = [item for item in items if item['name'] != name]
        return {'message': 'Item deleted'}

    def put(self, name):
        """
        Takes an item and json data
        If item exists, updates price
        If item does not exist, adds it to items
        Returns the latest data for the item regardless
        """

        data = Item.parser.parse_args()
        item = next((item for item in items if item['name'] == name), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
        else:
            item.update(data)
        return item

class Items(Resource):
    
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/item/<name>
api.add_resource(Items, '/items') # http://127.0.0.1/items

app.run(port=5000, debug=True)