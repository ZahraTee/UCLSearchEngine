#!flask/bin/python

#libraries
from flask import Flask, jsonify, request, make_response
import requests, json

#project
from searchimpl import searchapiutil, uclsearch, googlesearch, oursearch, judging

app = Flask(__name__)

queries = searchapiutil.read_queries()

#API start
@app.route('/')
@app.route('/query/')
def index():
  return make_response(open('templates/index.html').read())
  ##return "Hello, World! This is an api."#/

@app.route('/query/<int:id>')
def query_page(id):
  #if (id > 0 and id <= 49)
  return make_response(open('templates/index.html').read())
  ##return "Hello, World! This is an api."#/

@app.route('/api/search', methods=['GET'])
def search():
    query_id = request.args.get('query_id', -1, type = int)
  
    if query_id <= 0 or query_id > len(queries):
         return make_response(jsonify({'error': 'Query with id ' + str(query_id) + ' not found'}), 404)

    google_res = googlesearch.get_res(query_id)
    print("Google results: " + str(len(google_res)))
    
    ucl_res = uclsearch.get_res(query_id)
    print("UCL results: " + str(len(ucl_res)))
    
    ours_res = oursearch.get_res(query_id)
    print("Our results: " + str(len(ours_res)))
    
    results = []
    results = judging.processresults(google_res, ucl_res, ours_res)
    return make_response(json.dumps(results), 200)

@app.route('/api/query', methods=['GET'])
def get_queries():
    return make_response(jsonify({'queries': queries}), 200)

@app.route('/api/query/<int:query_id>', methods=['GET'])
def get_query(query_id):
    return make_response(jsonify(queries[query_id - 1]), 200)

@app.route('/api/judgement/<int:query_id>', methods=['POST'])
def show_post(query_id):
    data = request.json
    if query_id <= 0 or query_id > len(queries):
         return make_response(jsonify({'error': 'Query with id ' + str(query_id) + ' not found'}), 404)
    judging.parsejudgements(data, query_id)
    return json.dumps(request.json)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)