import requests

from searchimpl import searchapiutil

def parse_results(link):
	#TODO add id
	results = requests.get(link)
	results = results.json()['items']
	
	for i in range(len(results)):
		results[i] = { 'title' : results[i]['title'],
			'desc' : results[i]['htmlSnippet'],
			'link' : searchapiutil.normalize(results[i]['link']) }
	return results

def get_res(query):
    credentials = searchapiutil.read_credentials()
    res = parse_results('https://www.googleapis.com/customsearch/v1?key=' + credentials['key'] 
        + '&cx=' + credentials['cx'] 
        + '&q=' + query + '&num=10&start=1')
    res = res + parse_results('https://www.googleapis.com/customsearch/v1?key=' + credentials['key'] 
        + '&cx=' + credentials['cx'] 
        + '&q=' + query + '&num=10&start=11')
    return res
