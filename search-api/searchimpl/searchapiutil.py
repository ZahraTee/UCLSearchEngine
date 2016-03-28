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