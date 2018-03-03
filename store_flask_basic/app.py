from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'My Store',
        'items': [
            {
                'name': 'Item 1',
                'price': 15.99
            }
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')


# ENDPOINTS

# create a new store with a given name
# POST /store data: {name:}
@app.route('/store', methods = ['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


# get a store with a given name and return data about it
# GET /store/<string:name>
@app.route('/store/<string:name>') # http://127.0.0.1:5000/store/some_name
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'Store not found'})


# get a list of stores
# GET /store
@app.route('/store')
def get_store_list():
    return jsonify({'stores': stores})


# create an item inside a specific store with a given name
# POST /store<string:name>/item
@app.route('/store/<string:store_name>/item', methods = ['POST'])
def create_item_in_store(store_name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == store_name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'Store {} not found'.format(store_name)})


# get all the items in a specific store
# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_all_items_in_store(name):
    
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'No store called {}'.format(name)})


app.run(port = 5000)