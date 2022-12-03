import requests
import bs4
from datetime import date,timedelta

const= 'https://panorama.pub'

def get_linked (link):    
    req = requests.get(link)
    return req

def get_links_from_request(request, file_writer):
    soup = bs4.BeautifulSoup(request.text, 'html') 
    anchors=soup.find_all('a')
    for i in range(0,len(anchors)):
        links=anchors[i].get('href')
        if(links is not None):
            if(not links.find('/news')==-1):
                print(date, const+links)
                file_writer.write(const+links+"\n") 

def parse_links_from_chapter(date_begin,date_end,chapter):
    file_writer=open('Links.txt','a')
    if(chapter=='politics' or chapter=='society'):
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
        while (date!=date_end):
            link = const+"/"+chapter+"/"+str(date.day)+"-"+str(date.month)+"-"+str(date.year)
            date=date-timed             
            req = get_linked(link)
            if(req.status_code == 200):
                get_links_from_request(req, file_writer)
            else:
                print("Not connected to link", link)
    else:
        page = 1
        link = const+"/"+chapter+"?page="+page
        req = get_linked(link)
        while(req.status_code == 200):
            get_links_from_request(req, file_writer)
            page = page + 1
            link = const+"/"+chapter+"?page="+page
            req = get_linked(link)
                
    file_writer.close()    

if(__name__ == "__main__"): 
   #parse_links_from_chapter(date(2022,11,29),date(2022,11,10),'politics')
   date_begin=date(2022,11,29)
   date_end=date(2022,11,10) 
   #date_begin>data_end