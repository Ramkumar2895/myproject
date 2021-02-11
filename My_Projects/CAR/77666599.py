from time import gmtime, strftime
from bs4 import BeautifulSoup
import requests
import html5lib
import time
import re
import os
import carcommon
from datetime import datetime

with open('77666599_Output.txt','w')as f:
    f.write("Issu_Id"+"\t"+"Date"+"\t"+"Year"+"\t"+"Vol_No"+"\t"+"Start_page_No"
    +"\t"+"End_page_No"+"\t"+"Pdf_link"+"\n")


def clean(text):
    text = re.sub(r'<[^>]*?>','',str(text))
    text = re.sub(r'\s+', ' ', str(text))
    text = re.sub(r'^\s*', '', str(text))
    text = re.sub(r'\s*$', '', str(text))
    text = re.sub(r'\s+\s+', '', str(text))
    text = re.sub(r'\t', '', str(text))
    text = re.sub(r'&amp;', '&', str(text))
    return text

id = 77666599	
name = 'ZWF Zeitschrift fuer Wirtschaftlichen Fabrikbetrieb'


form_data= {'redirectUri':'/loi/zwf',
'loginUri':'/action/showLogin?uri=%2Floi%2Fzwf',
'login':'s.cecil@elsevier.com',
'password':'bd2227',
'savePassword':'1',
'submit':'Sign In'}

main_url  = "https://www.nul-online.de/"
pdf_link =  "https://www.hanser-elibrary.com"
      
content_url = requests.post('https://www.hanser-elibrary.com/action/doLogin',data = form_data)
data = content_url.content
soup = BeautifulSoup(data,'html5lib')
newsTitle = PageIssue = PageNumber = doi_no = str(None)
content = re.findall(r'ul\s*class\=\"loiList\">[\w\W]*?loiTocUrl([\w\W]*?)ul\s*class\=\"loiList\">[\w\W]*?loiTocUrl',str(soup))[0]
issu_id = re.findall(r'a\s*href\=\"[^>]*?\">([^>]*?)\,',str(content))
inner_links = re.findall(r'a\s*href\=\"([^>]*?)\">',str(content))
count = 1
for i in inner_links:
    content_url2 = requests.get(i)
    data2 = content_url2.content
    soup2 = BeautifulSoup(data2,'html5lib')
    inner_content = re.findall(r'tbody([\w\W]*?)<\/tr>',str(soup2))
    for org_inner_content in inner_content:
        issue_id = re.findall(r'Vol\.\s*[\w\W]*?No\s*[^>]*?([^>]*?)\.',str(org_inner_content))[0]
        date = re.findall(r'<div class="art_meta">[^>]*?([A-z]*?\s*[\d]{4})',str(org_inner_content))[0]
        year = re.findall(r'<div class="art_meta">[^>]*?[A-z]*?\s*([\d]{4})',str(org_inner_content))[0]
        vol_no = re.findall(r'<div class="art_meta">[^>]*?[A-z]*?\s*[\d]{4}\,\s*Vol\.\s*([^>]*?)\,',str(org_inner_content))[0]
        page_start = re.findall(r'Pages\:\s*([^>]*?)\–',str(org_inner_content))[0]
        page_end = re.findall(r'Pages\:\s*[^>]*?\–([^>]*?)<',str(org_inner_content))[0]
        pdf_l = re.findall(r'ref\s*nowrap\s*pdf\"\s*href\=\"([^>]*?)\"',str(org_inner_content))[0]
        org_pdf_link = pdf_link+pdf_l
        
        with open('77666599_Output.txt','a')as f:
            f.write(str(clean(issue_id))+"\t"+str(clean(date))+"\t"+str(clean(year))+"\t"+str(clean(vol_no))+"\t"+str(clean(page_start))
            +"\t"+str(clean(page_end))+"\t"+str(clean(org_pdf_link))+"\n")

        parsedNews = {'newsTitle':newsTitle, 'PageDate':date, 'PageDOI':doi_no, 'PageVolume':vol_no, 'PageIssue':PageIssue, 'PageNumber':PageNumber,'Year':year,'startyear':page_start,'Endyear':page_end,'PDF_URL':org_pdf_link}
        PDF_Status = carcommon.download_PDF(parsedNews,id,name,main_url)
        # time.sleep(20)
        if PDF_Status == 'Failed':
            Downloaded_status = 'Failed'
        else:
            Downloaded_status = 'Downloaded'
        date_format = datetime.strftime(carcommon.current_datetime, '%Y-%m-%d %H:%M:%S')
        publish_date = carcommon.dateconvert(date)
        carcommon.insert_data(Source_ID=str(id),D_Vol=str(vol_no),D_Issu=str(issue_id),Workflow="PDF",d_TO_Curl=str(i),Dart_URL=str(clean(org_pdf_link)),D_Location=str(count),Pub_Year=str(year),Pub_Date=str(publish_date),A_ID=str(None),artno=str(None),DOI=str(doi_no),F_Page=str(None),L_Page=str(None),filepath=str(PDF_Status),downloadtype = Downloaded_status,MainLink=str(None),date_format=str(date_format),title=None)
        count +=1

