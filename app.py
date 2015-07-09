#!flask/bin/python
from flask import abort, Flask, jsonify, make_response, request

app = Flask(__name__)

books = [
    {
        'id': 1,
        'title': 'Learn C++',
        'checkedIn': True
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'checkedIn': True
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Book creation failed'}), 400)

@app.route('/api/v1.0/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})

@app.route('/api/v1.0/books', methods=['POST'])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id': books[-1]['id'] + 1,
        'title': request.json['title'],
        'checkedIn': True
    }
    books.append(book)
    return jsonify({'book': book}), 201

@app.route('/api/v1.0/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    return jsonify({'book': book[0]})

@app.route('/api/v1.0/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    book[0]['title'] = request.json.get('title', book[0]['title'])
    book[0]['done'] = request.json.get('done', book[0]['done'])
    return jsonify({'book': book[0]})

@app.route('/api/v1.0/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    books.remove(book[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)