from bs4 import BeautifulSoup
import requests

from searchimpl import searchapiutil

def strip_string(item):
	return item.replace("\t", "").replace("\r", "").replace("\n", "").replace("  ", "")


def parse_item(item):
	#TODO add id
	
	desc = item.find(attrs={'class': 'result__summary'})
	desc.attrs = {}
	desc = str(desc)
	desc = strip_string(desc)
	
	title = item.find(attrs={'class': 'result__title'}).get_text()
	title = strip_string(title)
	
	link = item.find(attrs={'class': 'result__link'}).get_text()
	link = strip_string(link)
	link = searchapiutil.normalize(link)
	
	return { 'title' : title,
			  'desc' : desc,
			  'link' : link }

def parse_results(link):
	html_doc = requests.get(link).text
	soup = BeautifulSoup(html_doc, 'html.parser')
	soup = soup.find_all(attrs={'class': 'result__item--web'})
	results = []
	for item in soup:
		results.append(parse_item(item))
	return results

def get_res(query):
    
    results = parse_results('http://search2.ucl.ac.uk/s/search.html?query='
    	+ query + '&collection=website-meta&profile=_website')
    results = results + parse_results('http://search2.ucl.ac.uk/s/search.html?query='
    	+ query + '&collection=website-meta&profile=_website&start_rank=11')
    return results