import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 200
        return {'message': 'Item not found'}, 404

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

class ItemList(Resource):
    
    def get(self):
        """ Returns all items """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        row = result.fetch()
        connection.close()

        return {'items': row}