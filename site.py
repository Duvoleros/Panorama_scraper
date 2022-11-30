import requests
import bs4
import urllib.parse
import os

def get_linked (link):
    
    req = requests.get(link)
    return req

def clean_current_dir():
    file_list = (os.listdir())
    for i in range(0,len(os.listdir())):
        if(len(file_list[i].split('.')[0])<=3):
            os.remove(os.getcwd()+r'\\'+file_list[i])
            
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
    return string

def Parse_news_text(request):
    if(request.status_code == 200):
        html_source = bs4.BeautifulSoup(request.text,'lxml')
        texts = html_source.find_all('div',attrs={"itemprop":"articleBody"})[0].find_all('p')
        for i in range (0,len(texts)):
            texts[i] = Html_replace(texts[i].contents)
        return (texts)
    else:
        return ("Not connected to link")
    
def Parse_news_title(request):
    if(request.status_code == 200):
        html_source = bs4.BeautifulSoup(request.text,'lxml')
        title = html_source.find_all('h1')[0]
        title = Html_replace(title.contents)
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
        return ("Not connected to link")
    else:
        return ("Not connected to link")   
    
main_link = 'https://panorama.pub/news/smi-kreml-santaziruet-papu-rimskogo'
req = get_linked(main_link)
print(os.getcwd())
clean_current_dir()
print(Parse_news_picture(req))
print(Parse_news_title(req))
print(Parse_news_text(req))