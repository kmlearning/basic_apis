from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument('store_id', 
        type=int,
        required=True,
        help="Store cannot be left blank"
    )


    @jwt_required()
    def get(self, name):
        """ Takes an item name and returns the item """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        """ 
        Takes an item name and json data and adds it to stored items
        Returns the item if accepted, returns 400 and error if already exists
        """
        if ItemModel.find_by_name(name):
            return {"message": "An item with name {} already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500 # Internal server error

        return item.json(), 201

    def put(self, name):
        """
        Takes an item and json data
        If item exists, updates price
        If item does not exist, adds it to items
        Returns the latest data for the item regardless
        """
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()

    def delete(self, name):
        """
        Delete an item from the items
        Return message if successful
        """
        item = ItemModel.find_by_name(name)
        item.delete_from_db()

        return {'message': 'Item deleted'}

class ItemList(Resource):
    
    def get(self):
        """ Returns all items """
        return {'items': [item.json() for item in ItemModel.query.all()]}

