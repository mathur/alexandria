#!flask/bin/python
from flask import abort, Flask, jsonify, make_response, request

app = Flask(__name__)

items = [
    {
        'id': 1,
        'name': 'Learn C++',
        'type': 'book',
        'checkedIn': True
    },
    {
        'id': 2,
        'name': 'Learn Python',
        'type': 'book',
        'checkedIn': True
    },
    {
        'id': 3,
        'name': 'Spark Core',
        'type': 'hardware',
        'checkedIn': False
    }
]


"""
Return the json of a 404 error
"""
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


"""
Return the json of a 400 error
"""
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


"""
Get either a list of items, a specific item by id, or all the items of a certain type
"""
@app.route('/api/v1.0/items', methods=['GET'])
def get_items():
    if 'id' in request.args:
        item = [item for item in items if str(
            item['id']) == request.args['id']]
        if len(item) == 0:
            abort(404)
        return jsonify({'item': item[0]})
    elif 'type' in request.args:
        item = [item for item in items if item['type'] == request.args['type']]
        if len(item) == 0:
            abort(404)
        elif len(item) == 1:
            return jsonify({'item': item})
        else:
            return jsonify({'items': item})
    elif 'checkedin' in request.args:
        item = [item for item in items if str(item['checkedIn']).lower() == request.args['checkedin'].lower()]
        if len(item) == 0:
            abort(404)
        elif len(item) == 1:
            return jsonify({'item': item})
        else:
            return jsonify({'items': item})
    else:
        return jsonify({'items': items})


"""
Add a new item to the database
"""
@app.route('/api/v1.0/items', methods=['POST'])
def create_item():
    if not request.json or not 'name' in request.json or not 'type' in request.json:
        abort(400)
    item = {
        'id': items[-1]['id'] + 1,
        'name': request.json['name'],
        'type': request.json['type'],
        'checkedIn': True
    }
    items.append(item)
    return jsonify({'item': item}), 201


"""
Update an item by id
"""
@app.route('/api/v1.0/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'type' in request.json and type(request.json['type']) != unicode:
        abort(400)
    if 'checkedIn' in request.json and type(request.json['done']) is not bool:
        abort(400)
    item[0]['name'] = request.json.get('name', item[0]['name'])
    item[0]['checkedIn'] = request.json.get('checkedIn', item[0]['checkedIn'])
    return jsonify({'item': item[0]})


"""
Delete an item by id
"""
@app.route('/api/v1.0/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    items.remove(item[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
