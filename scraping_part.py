import time
import os
import pandas as pd
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

Options=webdriver.ChromeOptions()
Options.add_argument('incognito')
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=Options)
urls=[]
try:
    startUrl='https://brainlox.com/courses/category/technical'
    driver.get(startUrl)
    time.sleep(4)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    page_table=soup.find('div',class_='courses-area courses-section pt-100 pb-70').find_all('div',class_='single-courses-box')
    for each_course in page_table:
        course_link='https://brainlox.com'+ each_course.find('a')['href']
        urls.append(course_link)

    for each_link in urls:
        driver.get(each_link)
        time.sleep(4)
        soup1=BeautifulSoup(driver.page_source,'html.parser')

        try:
            course_title=soup1.find('div',class_='page-title-content').find('h2').text.strip()
        except Exception as e:
            print('Exception at Title',e)
        try:
            course_fee=soup1.find('ul',class_='info').text.strip()
        except Exception as e:
            print('Exception at course fee',e)
        try:
            course_description=soup1.find('div',class_='courses-overview').text.strip()
        except Exception as e:
            print('Exception at description',e)
        
        driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div[2]/div/div[1]/div[1]/div/ul/li[2]').click()
        time.sleep(1)
        # driver.find_element(By.CLASS_NAME,'react-tabs__tab').click()
        try:
            curriculum=driver.find_element(By.CSS_SELECTOR,'div.courses-curriculum').text.strip()
        except Exception as e:
            print('Exception at Curriculum',e)
        full_description=course_description+'\n''\n'+ curriculum + '\n''\n'+course_fee
        data_df = {'Course Title': [course_title], 'Course URL': [each_link], 'Course Description': [full_description]}
    
        df=pd.DataFrame(data_df)
        csv_filename='scraped_data.csv'
        write_header = not os.path.isfile(csv_filename)
        with open(csv_filename,mode= 'a',encoding='utf-8') as f:
            df.to_csv(f,index=False,lineterminator='\n',header=write_header)
            
except Exception as e:
    print('Exception at beginning',e)