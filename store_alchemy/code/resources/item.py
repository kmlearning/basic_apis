import sqlite3
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
        item = ItemModel(name, data['price'])

        try:
            item.insert()
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
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message': 'An error occurred'}, 500
        else:
            try:
                updated_item.update()
            except:
                return {'message': 'An error occurred'}, 500
        return updated_item.json()

    def delete(self, name):
        """
        Delete an item from the items
        Return message if successful
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

class ItemList(Resource):
    
    def get(self):
        """ Returns all items """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}
