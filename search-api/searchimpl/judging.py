from flask import make_response
from datetime import datetime
import random

def devidebuckets(bucket_id, prefix, res):
	results = []
	for i in range(len(res)):
		id = prefix + str(i)
		id = id[::-1]
		id = hash(id) % 4 #devide in 4 buckets
		if id == bucket_id:
			results.append( {
				'title' : res[i]['title'],
				'link' : res[i]['link'],
				'desc' : res[i]['desc']
				})
	return results



def processresults(google_res, ucl_res, ours_res):
	#eliminate duplicate links
	links_dict = {}
	for i in range(len(google_res)):
		links_dict[google_res[i]['link']] = True
	
	i = 0
	while i < len(ucl_res):
		if ucl_res[i]['link'] in links_dict:
			#print(i)
			ucl_res.pop(i)
			i = i - 1
		i = i + 1

	i = 0
	while i < len(ours_res):
		if ours_res[i]['link'] in links_dict:
			#print(i)
			ours_res.pop(i)
			i = i - 1
		i = i + 1

	results = google_res + ucl_res + ours_res 
	random.shuffle(results)
	return results

def parsejudgements(data, query_id):
    filename = "judgement." + "query_" + str(query_id) + "." + datetime.now().strftime('%Y%m%d%H%M%S') + ".out"
    output_file = open("judgement_results/" + filename, "w" )
    judgements = data

    for i in range(len(judgements)):
        if 'relevance' in judgements[i].keys():
            relevance = judgements[i]['relevance']
            print("we got here ok too!")
            if relevance >= 0 and relevance < 3:
                output_file.write(str(query_id) + " " + judgements[i]['link'] + " " + str(relevance) + "\n")
            else:
                return make_response(jsonify({'error': 'Incorrect relevance judgement for ' + str(judgements[i]['link']) + ' judged as ' + str(relevance)}), 404)
        else:
             return make_response(jsonify({'error': 'Judgement not present for ' + str(judgements[i]['link'])}), 404)
