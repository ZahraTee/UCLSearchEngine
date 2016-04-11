def devidebuckets(bucket_id, prefix, res):
	results = []
	for i in range(len(res)):
		id = prefix + str(i)
		id = id[::-1]
		id = hash(id) % 4 #devide in 3 buckets
		if id == bucket_id:
			results.append( {
				'title' : res[i]['title'],
				'link' : res[i]['link'],
				'desc' : res[i]['desc']
				})
	return results



def bucketresults(bucket_id, google_res, ucl_res, ours_res):
	results = []
	#return ucl_res
	return devidebuckets(bucket_id, "1", google_res) + devidebuckets(bucket_id, "2", ucl_res) 
	+ devidebuckets(bucket_id, "3", ours_res)