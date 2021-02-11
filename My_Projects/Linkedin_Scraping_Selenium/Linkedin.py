from bs4 import BeautifulSoup
import html5lib
import re
import time
from time import gmtime, strftime
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import os

def clean(text):
    text = re.sub(r'<[^>]*?>','',str(text))
    text = re.sub(r'\s+', ' ', str(text))
    text = re.sub(r'^\s*', '', str(text))
    text = re.sub(r'\s*$', '', str(text))
    text = re.sub(r'\s+\s+', '', str(text))
    text = re.sub(r'\t', '', str(text))
    return text

with open("Linkedin_Output.txt",'a') as file:
    file.write("Page_No"+"\t"+"Company_Name"+"\t"+"Country"+"\t"+"Name"+"\t"+"Job"+"\t"+"Current_Job"+"\t"+"Link"+"\n")

website_URL = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
driver = webdriver.Chrome()
driver.get(website_URL)
driver.maximize_window()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="username"]').send_keys('')
time.sleep(1)
driver.find_element_by_xpath('//*[@id="password"]').send_keys('')
time.sleep(1)
driver.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button').click()
time.sleep(4)

with open("input.txt","r",encoding = "utf-8") as ip:
    for input_s in ip:
        company = input_s.split('\t')[0]
        country = input_s.split('\t')[1]
        org_country = country.strip()
        driver.find_element_by_css_selector('.search-global-typeahead__input.always-show-placeholder').send_keys(str(company))
        time.sleep(2)
        driver.find_element_by_css_selector('.search-global-typeahead__controls').click()
        time.sleep(2)
        driver.find_elements_by_css_selector('.search-s-facet__button.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--2.artdeco-button--secondary.ember-view')[1].click()
        time.sleep(3)
        driver.find_elements_by_css_selector('input[type=text]')[1].send_keys(str(org_country))
        time.sleep(2)
        driver.find_elements_by_css_selector('.search-typeahead-v2__hit.ember-view')[0].click()
        time.sleep(2)
        driver.find_elements_by_css_selector('.facet-collection-list__apply-button.ml2.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view')[1].click()
        time.sleep(2)
        ram = driver.page_source
        if re.search(r'artdeco-button\_\_text\">\s*Next\s*<\/span>',str(ram),re.I) is not None:
            scroll = driver.find_element_by_tag_name('body')
            for i in range(0,4):
                scroll.send_keys(Keys.PAGE_DOWN)
                time.sleep(2)
            
            pc = driver.find_element_by_css_selector('.artdeco-pagination__pages.artdeco-pagination__pages--number')
            lis = pc.find_elements_by_css_selector('li')
            cc = lis[len(lis)-1].text
            page = int(cc)
            for i in range(page):
                for i in range(0,4):
                    scroll.send_keys(Keys.PAGE_DOWN)
                    time.sleep(1)
                content = driver.page_source
                org_content = BeautifulSoup(content,'html5lib')
                for cont in org_content.select('.search-result__info'):
                    try:
                        name = cont.select('.actor-name')[0].text
                        print(name)
                    except Exception as e:
                        print(e)
                        name = ""
                    try: 
                        job = cont.select('.subline-level-1.t-14.t-black.t-normal.search-result__truncate')[0].text.strip()
                        print(job)
                    except Exception as e:
                        print(e)
                        job = ""
                    try:
                        current = cont.select('.mt2.t-12.t-black--light.t-normal.search-result__snippets-black')[0].text.strip()
                        print(current)
                    except Exception as e:
                        print(e)
                        current = ""  
                    link = cont.select_one('.search-result__result-link.ember-view').get('href')
                    org_link = "https://www.linkedin.com"+link
                    print(org_link)
                    with open("Linkedin_Output.txt",'a',encoding = 'utf-8') as file:
                        file.write(str(page)+"\t"+str(clean(company))+"\t"+str(clean(country))+"\t"+str(clean(name))+"\t"+str(clean(job))+"\t"+str(clean(current))+"\t"+str(clean(org_link))+"\n")
                    time.sleep(2)
                driver.find_element_by_css_selector('.artdeco-pagination__button.artdeco-pagination__button--next.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view').click()
            driver.find_element_by_css_selector('.nav-main__inbug-container').click()
            time.sleep(2)
        if re.search(r'<h1\s*class\=\"t\-20\s*t\-black\s*t\-normal\s*mb2\">No\s*results\s*found\.<\/h1>',str(ram),re.I) is not None:
            driver.find_element_by_css_selector('.nav-main__inbug-container').click()
            time.sleep(3)
        else:
            scroll = driver.find_element_by_tag_name('body')
            for i in range(0,4):
                scroll.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
            content = driver.page_source
            org_content = BeautifulSoup(content,'html5lib')
            for cont in org_content.select('.search-result__info'):
                try:
                    name = cont.select('.actor-name')[0].text
                    print(name)
                except Exception as e:
                    print(e)
                    name = ""
                try: 
                    job = cont.select('.subline-level-1.t-14.t-black.t-normal.search-result__truncate')[0].text.strip()
                    print(job)
                except Exception as e:
                    print(e)
                    job = ""
                try:
                    current = cont.select('.mt2.t-12.t-black--light.t-normal.search-result__snippets-black')[0].text.strip()
                    print(current)
                except Exception as e:
                    print(e)
                    current = ""  

                link = cont.select_one('.search-result__result-link.ember-view').get('href')
                org_link = "https://www.linkedin.com"+link
                print(org_link)
                with open("Linkedin_Output.txt",'a',encoding = 'utf-8') as file:
                    file.write(str("1")+"\t"+str(clean(company))+"\t"+str(clean(country))+"\t"+str(clean(name))+"\t"+str(clean(job))+"\t"+str(clean(current))+"\t"+str(clean(org_link))+"\n")
            time.sleep(1)
            driver.find_element_by_css_selector('.nav-main__inbug-container').click()
            time.sleep(2)
            
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
 












 
     
       
            # driver.back()
            # time.sleep(2)
            # driver.find_element_by_css_selector('.search-global-typeahead__input.always-show-placeholder').clear()
            # time.sleep(2)
            # driver.find_element_by_css_selector('.artdeco-pagination__button.artdeco-pagination__button--next.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view').click()
            # time.sleep(5)


##        except:
##            for i in range(0,4):
##                scroll.send_keys(Keys.PAGE_DOWN)
##                time.sleep(2)
##            content = driver.page_source
##            org_content = BeautifulSoup(content,'html5lib')
##            for cont in org_content.select('.search-result__info'):
##                try:
##                    name = cont.select('.actor-name')[0].text
##                    print(name)
##                    
##                except Exception as e:
##                    print(e)
##                    name = ""
##                try: 
##                    job = cont.select('.subline-level-1.t-14.t-black.t-normal.search-result__truncate')[0].text.strip()
##                    print(job)
##                except Exception as e:
##                    print(e)
##                    job = ""
##                try:
##                    current = cont.select('.mt2.t-12.t-black--light.t-normal.search-result__snippets-black')[0].text.strip()
##                    print(current)
##                except Exception as e:
##                    print(e)
##                    current = ""  
##
##                link = cont.select_one('.search-result__result-link.ember-view').get('href')
##                org_link = "https://www.linkedin.com"+link
##                print(org_link)
##                with open("Linkedin_Output5.txt",'a',encoding = 'utf-8') as file:
##                    file.write(str(page)+"\t"+str(clean(company))+"\t"+str(clean(country))+"\t"+str(clean(name))+"\t"+str(clean(job))+"\t"+str(clean(current))+"\t"+str(clean(org_link))+"\n")
####                    time.sleep(6)
##            driver.find_elements_by_css_selector('.nav-item__link.js-nav-item-link')[0].click()
##            time.sleep(5)













##            name = driver.find_elements_by_css_selector('.name.actor-name')
##            name2 = ([i.text for i in name ])
##            job = driver.find_elements_by_css_selector('.subline-level-1.t-14.t-black.t-normal.search-result__truncate')
##            job2 = ([i.text for i in job ])
##            current = driver.find_elements_by_css_selector('.mt2.t-12.t-black--light.t-normal.search-result__snippets-black')
##            current = ([i.text for i in current ])
##            driver.find_element_by_css_selector('.artdeco-pagination__button.artdeco-pagination__button--next.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view').click()

##        print ("CC:: ",cc)
##        input("***STOP2***")
##        driver.find_element_by_css_selector('.search-vertical-filter__dropdown-trigger-text.mr1').click()
##        time.sleep(2)
##        driver.find_element_by_css_selector('.search-vertical-filter__dropdown-list-item-button.t-14.t-black--light.t-bold.full-width.search-vertical-filter__dropdown-list-item-button--COMPANIES.ember-view').click()
##        time.sleep(2)
##        try:
##            driver.find_elements_by_css_selector('.search-result__title.t-16.t-black.t-bold')[0].click()
##            time.sleep(2)
##            s = driver.page_source
##            with open('inner_link.html','w',encoding = 'urf-8') as f:
##                f.write(str(s))
##            if re.search(r'Reactions',str(s),re.I) is not None:
##                driver.find_element_by_css_selector('.artdeco-modal__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view').click()
##            else:
##                pass
##            driver.find_elements_by_css_selector('.v-align-middle')[2].click()            
##            try:
##                page = cc
##                for i in range(page):
##                    scroll = driver.find_element_by_tag_name('body')
##                    for i in range(0,2):
##                        time.sleep(2)
##                        scroll.send_keys(Keys.PAGE_DOWN)
##                        time.sleep(2)
##                    name = driver.find_elements_by_css_selector('.name.actor-name')
##                    org_name = ([i.text for i in name ])
##                    print(org_name)
##                    job = driver.find_elements_by_css_selector('.subline-level-1.t-14.t-black.t-normal.search-result__truncate')
##                    org_job = ([i.text for i in job ])
##                    print(org_job)
##                    time.sleep(4)
##                    driver.find_element_by_css_selector('.artdeco-pagination__button.artdeco-pagination__button--next.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view').click()
##            except:
##                pass
##        except:
##            print('Companies Not Available')
##            time.sleep(2)
##            driver.find_elements_by_css_selector('.nav-item__link.js-nav-item-link')[0].click()
##            time.sleep(3)
    
##.artdeco-button__text
##a = "comp"
##for i in driver.find_elements_by_css_selector('.search-result__title.t-16.t-black.t-bold'):
##    
##    if i.text == a:
##        driver.find_elements_by_css_selector('.search-result__title.t-16.t-black.t-bold')[i].click()
##a = driver.page_source
##with open('out.html','a',encoding = 'utf-8') as f:
##    f.write(str(a))
##    f.close()
##driver.find_elements_by_css_selector('input[type=text]')[1].send_keys(Keys.TAB)
##time.sleep(2)
##driver.find_elements_by_css_selector('input[type=text]')[1].send_keys(Keys.SPACE)
##time.sleep(4)
##driver.find_elements_by_css_selector('.facet-collection-list__apply-button.ml2.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view')[1].click()
