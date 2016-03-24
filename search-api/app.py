#!flask/bin/python
from flask import Flask, jsonify, request, make_response
import requests

app = Flask(__name__)

def read_credentials():
    f = open('credentials', 'r')
    return {'key' : f.readline().rstrip('\n'), 'cx': f.readline().rstrip('\n')}

def read_queries():
    queries = []
    with open('queries', 'r') as f:
        query_id = 1
        category = 'unknown'
        for line in f:
            
            if line == '\n':
                continue

            if line[0] == '[':
                category = line[1:-2]
                continue
            
            queries.append({
                    'id': query_id,
                    'content' : line[:-1],
                    'category' : category
                })
            query_id += 1

    return queries

queries = read_queries()

def get_google_res(query):
    credentials = read_credentials()
    res = requests.get('https://www.googleapis.com/customsearch/v1?key=' + credentials['key'] 
        + '&cx=' + credentials['cx'] 
        + '&q=' + query + '&num=10&start=1')
    return res.json()


#API start
@app.route('/')
def index():
    return "Hello, World! This is an api."


@app.route('/api/search', methods=['GET'])
def search():
    query_id = request.args.get('query_id', -1, type = int)

    if query_id <= 0 or query_id > len(queries):
         return make_response(jsonify({'error': 'Query with id ' + str(query_id) + ' not found'}), 404)
    query_id -= 1
    
    google_res = get_google_res(queries[query_id]['content'])
    ucl_res = []
    ours_res = []
    
    return make_response(jsonify(
    	{'query': queries[query_id],
    	 'google' : google_res,
    	  'ucl': ucl_res,
    	  'ours': ours_res}), 200)

@app.route('/api/queries', methods=['GET'])
def get_queries():
    return make_response(jsonify({'queries': queries}), 200)

@app.route('/api/queries/<int:query_id>', methods=['GET'])
def get_query(query_id):
    return make_response(jsonify(queries[query_id - 1]), 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)