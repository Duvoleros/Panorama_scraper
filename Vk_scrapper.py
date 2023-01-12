import requests
import bs4
import os
import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

main_link = "https://m.vk.com/ia_panorama"

def generate_html(condition):

    
    driver = webdriver.Chrome(
        executable_path = os.getcwd()+"\chromedriver\chromedriver.exe"
    )
    driver.maximize_window()
    driver.get(main_link)

    actions = ActionChains(driver)
    #prototype of correct generation source
    for i in range(0,condition):  
        actions.scroll_by_amount(0,33000).perform()
        actions.scroll_by_amount(0,-1000).perform()
        if(i == 1):
            actions.send_keys(Keys.ESCAPE).perform()
        date_list = driver.find_elements(By.CLASS_NAME, "wi_info")
        print(len(date_list),i)
        time.sleep(1)
    html = driver.page_source #it was possible to save html to file, but it showed mistake with encoding
    driver.quit()
    return html



request = requests.get(main_link)
soup = bs4.BeautifulSoup(generate_html(1), 'lxml') 
news = soup.find_all("div",attrs={"class":"wall_item post--withRedesign"})
for i in range(0, len(news)):
    temp_news = news[i]
    text_ = news[i].find_all("div",attrs={"class":"pi_text"})
    print(text_)
    image_ = news[i].find_all("img",attrs={"class":"MediaGrid__imageSingle"})
    if(len(image_)>0):
        image_ = str(image_[0]).split('"')[-4]
        image_ = image_.replace("amp;","")
        print(image_)




