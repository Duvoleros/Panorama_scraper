import requests
import bs4
import urllib.parse
import os
import html5lib
from datetime import date,timedelta
def get_linked (link):
    
    req = requests.get(link)
    return req




const= 'https://panorama.pub'
chapter="politics"

date_begin=date(2022,11,26)
date_end=date(2022,11,20)
#date_begin>data_end
file_writter=open('Links.txt','w')
timed=timedelta(
    days=1,
    seconds=0,
    microseconds=0,
    milliseconds=0,
    minutes=0,
    hours=0,
    weeks=0
)
date=date_begin+timed
while True:
 date=date-timed 
 if(chapter=='politics' or chapter=='society'):
   link = const+"/"+chapter+"/"+str(date.day)+"-"+str(date.month)+"-"+str(date.year)
# else:
#    page=1
#    if(page==1):
#        link = const+"/"+chapter
#    else:
#        link=const+"/"+chapter+"?page="+page
 req = get_linked(link)
 if(req.status_code == 200):
     soup = bs4.BeautifulSoup(req.text, 'html') 
     anchors=soup.find_all('a')
     for i in range(0,len(anchors)):
      links=anchors[i].get('href')
      if(links is not None):
         if(not links.find('/news')==-1):
            file_writter.write(const+links+"\n")
 else:
    print("Not connected to link")
 if date==date_end:
    break
file_writter.close()