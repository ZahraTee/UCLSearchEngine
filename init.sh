#Crawling
cd crawler
scrapy crawl two
cd ..

#Compute PageRank
python PageRank.py

#Indexing
#Construct collection.spec file
find crawler/doc -type f | grep '.*\.txt' > terrier-core-4.1/etc/collection.spec
#Construct index
terrier-core-4.1/bin/trec_terrier.sh -i