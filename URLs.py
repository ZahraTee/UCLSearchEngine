import os

N = 200891

def construct():
    URL_PATH="crawler/url/"
    F = open("URLs.txt","w")
    for n in range(N):
        f=open(URL_PATH+str(n)+".txt","r")
        url = f.read()
        if url[-1]=='\n':
            url=url[:-1]
        f.close()
        F.write(url+"\n")
    F.close()

URLs = [""]*N
def fill():
    F = open("URLs.txt","r")
    for n in range(N):
        url = F.readline()
        if url[-1]=='\n':
            url=url[:-1]
        URLs[n]=url
    F.close()
