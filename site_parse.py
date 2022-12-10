import requests
import bs4
import urllib.parse
import os
from datetime import date,timedelta

def get_linked (link):
    
    req = requests.get(link)
    return req

def clean_current_dir():
    file_list = (os.listdir())
    for i in range(0,len(os.listdir())):
        if(len(file_list[i].split('.')[0])<=3):
            os.remove(os.getcwd()+'\\'+file_list[i])
            
def delete_file(file_name):
    os.remove(os.getcwd()+'\\'+file_name)
            
def Join_Stringlist(inner_item, symbol_1, symbol_2):
                inner_item = str(inner_item)
                str_list = inner_item.split(symbol_1)
                string_rez =str_list[0]
                for j in range (1,len(str_list)):
                     string_rez = string_rez + symbol_2 + str_list[j]
                return string_rez

def Html_replace(string):
    string = Join_Stringlist(string,"\n", " ")
    string = Join_Stringlist(string,"\\n", " ")
    string = Join_Stringlist(string,"\\xa0", " ")
    string = Join_Stringlist(string,"\xa0", " ")
    return string

def Parse_news_text(request):
    if(request.status_code == 200):
        html_source = bs4.BeautifulSoup(request.text,'lxml')
        texts = html_source.find_all('div',attrs={"itemprop":"articleBody"})[0].find_all('p')
        for i in range (0,len(texts)):
            texts[i] = Html_replace(texts[i].contents)
            texts[i] = texts[i].replace("['", '')
            texts[i] = texts[i].replace("']", '')
            texts[i] = texts[i].strip()
        texts = '\n'.join(texts)
        return (texts)
    else:
        return ("Not connected to link")
    
def Parse_news_title(request):
    if(request.status_code == 200):
        html_source = bs4.BeautifulSoup(request.text,'lxml')
        title = html_source.find_all('h1')[0]
        title = Html_replace(title.contents)
        title = title.replace("['", '')
        title = title.replace("']", '')
        title = title.strip()
        return title
    else:
        return ("Not connected to link")
    
def Parse_news_picture(request):
    if(request.status_code == 200):
        html_source = bs4.BeautifulSoup(request.text,'lxml')
        title = html_source.find_all('div',attrs={"class":"w-full h-auto backdrop-blur-xl"})
        title = str(title[0]).split(' ')
        href = ""
        for i in range(0, len(title)):
            if(title[i].find("data-bg-image-jpeg") != -1):
                href = title[i]
                break
        href = href.split('"')[1]
        name = href.split('/')[-1]
        if(get_linked(href).status_code == 200):
            open(name, 'wb').write(requests.get(href, allow_redirects=True).content)
            return name
    else:
        return ("Not connected to link")
    
def Parse_news_date(request):
    if(request.status_code == 200):
        html_source = bs4.BeautifulSoup(request.text,'lxml')
        title = html_source.find_all('div',attrs={"class":"flex flex-col gap-x-3 gap-y-1.5 flex-wrap sm:flex-row"})
        title = (title[0]).text
        title = title.split(' ')
        for i in range(0,len(title)):
            title[i] = Html_replace(title[i])
            title[i] = title[i].strip()
        timed=timedelta(
            days=1,
            seconds=0,
            microseconds=0,
            milliseconds=0,
            minutes=0,
            hours=0,
            weeks=0
        )
        if(title[0] == "позавчера,"):
            return date.today() - timed - timed
        elif(title[0] == "вчера,"):
            return date.today() - timed
        elif(title[0] == "сегодня,"):
            return date.today()
        else:
            day = int(title[0])
            year = int(title[2])
            month_switcher = {
                'янв.': 1,
                'февр.': 2,
                'мар.': 3,
                'апр.': 4,
                'мая': 5,
                'июн.': 6,
                'июл.': 7,
                'авг.': 8,
                'сент.': 9,
                'окт.': 10,
                'нояб.': 11,
                'дек.': 12
            }
            return date(year, month_switcher[title[1]], day)
    else:
        return ("Not connected to link") 

def Parse_page(main_link):
    req = get_linked(main_link)
    return (1, Parse_news_title(req), Parse_news_text(req), Parse_news_date(req), Parse_news_picture(req))    

if(__name__ == "__main__"):
    main_link = 'https://panorama.pub/news/ajfony-zabirali-noutbuki-aborigeny-v'    
    print(Parse_page(main_link))