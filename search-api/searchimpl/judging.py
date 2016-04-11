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

def bucketresults(bucket_id, google_res, ucl_res, ours_res):
	results = [devidebuckets(bucket_id, "1", google_res), devidebuckets(bucket_id, "2", ucl_res),
		devidebuckets(bucket_id, "3", ours_res)] 
	random.shuffle(results)
	#return ucl_res
	return results[0] + results[1] + results[2]

def parsejudgements(data, query_id, bucket_id):
    filename = "judgement." + "query_" + str(query_id) + ".bucket_" + str(bucket_id) + "." + datetime.now().strftime('%Y%m%d%H%M%S') + ".out"
    output_file = open(filename, "w" )
    judgements = data["results"]
    for i in range(len(judgements)):
        if 'relevance' in judgements[i].keys():
            relevance = judgements[i]['relevance']
            if relevance >= 0 and relevance < 3:
                output_file.write(str(query_id) + " " + judgements[i]['link'] + " " + str(relevance) + "\n")
            else:
                return make_response(jsonify({'error': 'Incorrect relevance judgement for ' + str(judgements[i]['link']) + ' judged as ' + str(relevance)}), 404)
        else:
             return make_response(jsonify({'error': 'Judgement not present for ' + str(judgements[i]['link'])}), 404)
