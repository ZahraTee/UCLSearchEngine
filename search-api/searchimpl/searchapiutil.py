import requests

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

#A Function which gets a url and normalize it, to avoid duplication of crawling
def normalize(url):
    if url[4]=='s':
        url = url[:4]+url[5:]
    s = url.find("#")
    if s!=-1:
        url = url[:s]
    if url[-1]=='/':
        url = url[:-1]
    return url

def check_if_html(link):
    if link.endswith(".pdf"):
        print(link + " not an html.")
        return False
    r = requests.head(link)
    print(link)
    if 'Content-Type' in r.headers.keys() and "text/html" in r.headers['Content-Type']:
        return True
    print(link + " not an html.")
    return False
