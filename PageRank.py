import os


EPSILON = 0.001
MIN_ITERATIONS=40
MAX_ITERATIONS=200
JUMP_PROBABILITY=0.2

PATH="/Users/walsaeed/GitHub/UCLSearchEngine/crawler"
URL_PATH=PATH+"/url"
LINKS_PATH=PATH+"/links"

N = len(os.listdir(URL_PATH))-2 #Excluding '.DS_Store' and 'about' files
#N=50

URL_INDEX_MAP= {}
for n in range(N):
    f = open(URL_PATH+"/"+str(n)+".txt","r")
    url = f.read()
    if url[-1]=='\n':
        url = url[:-1]
    URL_INDEX_MAP[url]=n

LINKS=[]
for n in range(N):
    LINKS+=[[]]
    f = open(LINKS_PATH+"/"+str(n)+".txt","r")
    for line in f:
        link = line
        if link[-1]=='\n':
            link=link[:-1]
        if link in URL_INDEX_MAP:
            LINKS[n]+=[URL_INDEX_MAP[link]]

PAGE_RANK=[1.0/N]*N
for T in range(MAX_ITERATIONS):
    NEW_RANK=[JUMP_PROBABILITY/N]*N
    for n in range(N):
        if len(LINKS[n])==0:
            continue
        x = PAGE_RANK[n]*(1.0-JUMP_PROBABILITY)/len(LINKS[n])
        for t in LINKS[n]:
            NEW_RANK[t]+=x
    if T>=MIN_ITERATIONS:
        DIST=0
        for i in range(N):
            DIST+=pow((NEW_RANK[i]-PAGE_RANK[i]),2)
        DIST=pow(DIST,0.5)
        PAGE_RANK=NEW_RANK
        if DIST<EPSILON:
            break
    else:
        PAGE_RANK=NEW_RANK

OUTPUT_FILE=open("PageRank.txt","w")
for n in range(N):
    OUTPUT_FILE.write(("%.30f" % PAGE_RANK[n])+"\n")
OUTPUT_FILE.close()
