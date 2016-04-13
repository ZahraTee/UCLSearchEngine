from bs4 import BeautifulSoup
import requests, json

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
	if searchapiutil.check_if_html(link):
		return {'title' : title,
			  'desc' : desc,
			  'link' : link,
			  'rank' : rank}
	return None
		

def parse_results(link, start_rank):
	html_doc = requests.get(link).text
	soup = BeautifulSoup(html_doc, 'html5lib')
	result_links = soup.find_all(attrs={'class': 'result__item--web'})
	results = []
	i = start_rank
	for item in result_links:
		parsed_result = parse_item(item, i)
		if parsed_result is not None:
			results.append(parsed_result)
			i = i + 1
	return results

def get_number_result_pages(link):
	html_doc = requests.get(link).text
	soup = BeautifulSoup(html_doc, 'html5lib')
	result_pages = soup.find("ol", {"class": "results-nav__list"})
	no_pages = len(result_pages.find_all("li", {"class": ""})) + 1
	print("Number of result pages for ucl search: " + str(no_pages))
	return no_pages

def get_res_from_website(query):
   	no_result_pages = get_number_result_pages('http://search2.ucl.ac.uk/s/search.html?query='
   			+ query + '&collection=website-meta&profile=_website')
   	results = []
   	for i in range(no_result_pages):
   		start_rank = i*10 + 1
   		results = results + parse_results('http://search2.ucl.ac.uk/s/search.html?query='
   			+ query + '&collection=website-meta&profile=_website&start_rank=' + str(start_rank), start_rank)
   		if len(results) >= 20:
   			break
   	return results[0:20]

def get_res(query_id):
	input_file = open("ucl_results/ucl_result_" + str(query_id) + ".json", "r")
	return json.load(input_file)