from bs4 import BeautifulSoup
import requests

from searchimpl import searchapiutil

def strip_string(item):
	return item.replace("\t", "").replace("\r", "").replace("\n", "").replace("  ", "")


def parse_item(item, rank):
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

	if rank != -1:
		return {'title' : title,
			  'desc' : desc,
			  'link' : link,
			  'rank' : rank}
	else:
		return { 'title' : title,
			  'desc' : desc,
			  'link' : link}		

def parse_results(link, start_rank):
	html_doc = requests.get(link).text
	soup = BeautifulSoup(html_doc, 'html5lib')
	soup = soup.find_all(attrs={'class': 'result__item--web'})
	results = []
	i = start_rank
	for item in soup:
		results.append(parse_item(item, i))
		if start_rank != - 1:
			i = i + 1
	return results

def get_res(query):
   	results = parse_results('http://search2.ucl.ac.uk/s/search.html?query='
   			+ query + '&collection=website-meta&profile=_website', 1)
   	results = results + parse_results('http://search2.ucl.ac.uk/s/search.html?query='
   			+ query + '&collection=website-meta&profile=_website&start_rank=11', 11)
   	return results