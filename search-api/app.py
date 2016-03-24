#!flask/bin/python
from flask import Flask, jsonify, request, make_response
import requests

app = Flask(__name__)

def read_credentials():
    f = open('credentials', 'r')
    return {'key' : f.readline().rstrip('\n'), 'cx': f.readline().rstrip('\n')}

def get_google_res():
    credentials = read_credentials()
    res = requests.get('https://www.googleapis.com/customsearch/v1?key=' + credentials['key'] + '&cx=' + credentials['cx'] + '&q=lectures&num=10&start=1')
    return res.json()

@app.route('/')
def index():
    return "Hello, World! This is an api."


@app.route('/api/search', methods=['GET'])
def get_tasks():
    query = request.args.get('q')
    google_res = get_google_res()
    ucl_res = []
    ours_res = []
    return jsonify(
    	{'query': query,
    	 'google' : google_res,
    	  'ucl': ucl_res,
    	  'ours': ours_res}), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)