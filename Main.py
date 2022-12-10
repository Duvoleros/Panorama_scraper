import requests
import bs4
from datetime import date,timedelta
import sqlite3
import site_parse

const = 'https://panorama.pub'
database_name = "panorama.db"

def get_linked (link):    
    req = requests.get(link)
    return req

def get_links_from_request(request, file_writer):
    soup = bs4.BeautifulSoup(request.text, 'lxml') 
    anchors=soup.find_all('a')
    for i in range(0,len(anchors)):
        links=anchors[i].get('href')
        if(links is not None):
            if(not links.find('/news')==-1):
                print('\t link ', const+links)
                insert_to_db(const+links) 

def parse_links_from_chapter(date_begin,date_end,chapter):
    print("Start parsing links from chapter ", chapter) 
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
    print("End parsing links from chapter ", chapter)    

def convert_img_to_BLOB(filename):
    #convert digital data to binary format and delete the source file
    my_file = open(filename, 'rb')
    blob = my_file.read()
    my_file.close()
    site_parse.delete_file(filename)
    return blob

def check_news_by_title(title,database):
    find_cursor = database.cursor()
    find_cursor.execute("SELECT title FROM news;")
    titles_list = find_cursor.fetchall()
    for i in range (0, len(titles_list)):
        if(title == titles_list[i]):
            return -1
    find_cursor.execute("SELECT COUNT (1) FROM news;")
    id = find_cursor.fetchone()[0] + 1
    find_cursor.close()
    return id

def insert_to_db(link):
    database = sqlite3.connect(database_name)
    cursor = database.cursor()
    print("Connected to SQLite")
    sqlite_insert_blob_query = """ INSERT INTO news
                                    (id, title, describtion, date, photo) VALUES (?, ?, ?, ?, ?);"""
    news_title = site_parse.Parse_news_title(get_linked(link))
    id = check_news_by_title(news_title, database)    
    if (id!=-1): #function not completed
        data_tuple = site_parse.Parse_page(link)
        data_tuple = list(data_tuple)
        data_tuple[0] = id
        data_tuple[3] = str(data_tuple[3])
        data_tuple[4] = convert_img_to_BLOB(data_tuple[4])
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        database.commit()
        print("Image successfully inserted as a BLOB into a table")
    else:
        print("News is already in the base")
    cursor.close()        
    print("Disconnected from SQLite")
    
        
def launch_news_DB():
    database = sqlite3.connect(database_name)
    cursor = database.cursor()
    print("Connected to SQLite")
    cursor.execute("""CREATE TABLE IF NOT EXISTS news(
    id INT PRIMARY KEY,
    title TEXT,
    describtion TEXT,
    date TEXT,
    photo BLOB);
    """)
    database.commit()
    print("Launch script was executed")
    
def parse_all_news_this_year():
    #
    return
    

launch_news_DB()   
parse_links_from_chapter(date(2022,11,29),date(2022,11,23),'society')
#date_begin>data_end
    
