import linecache

def get_res(query_id):
	results = []
	rank = 0
	with open("BM25F_1.res", "r") as f:
		for line in f:
			tokens = line.split(" ")
			if tokens[0] == str(query_id):
				rank = rank + 1
				#print(rank)
				filename = tokens[2].split("/")
				filename = filename[len(filename) - 1]
				filename = filename.split(".")
				filename = filename[0]
				link = linecache.getline("URLs.txt", int(filename) + 1).strip() #lineache.getline works from 1 to len
				results.append({#'title' : title, no title
			  		#'desc' : desc, #no description
			  		'link' : link,
			  		'rank' : rank})
				print(link)
	return results	