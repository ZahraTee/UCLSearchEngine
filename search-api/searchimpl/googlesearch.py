import requests
import json

from searchimpl import searchapiutil

def parse_results(link, start_rank):
	#TODO add id
	results = requests.get(link)
	results = results.json()['items']
	
	for i in range(len(results)):
		results[i] = { 'title' : results[i]['title'],
		'desc' : results[i]['htmlSnippet'],
		'link' : searchapiutil.normalize(results[i]['link']),
		'rank' : (start_rank + i) }
	return results

def get_res_from_api(query):
    credentials = searchapiutil.read_credentials()
    res = parse_results('https://www.googleapis.com/customsearch/v1?key=' + credentials['key'] 
        + '&cx=' + credentials['cx'] 
        + '&q=' + query + '&num=10&start=1', 1)
    res = res + parse_results('https://www.googleapis.com/customsearch/v1?key=' + credentials['key'] 
        + '&cx=' + credentials['cx'] 
        + '&q=' + query + '&num=10&start=11', 11)
    return res

def get_res(query_id):
	input_file = open("google_results/google_result_" + str(query_id) + ".json", "r")
	return json.load(input_file)

