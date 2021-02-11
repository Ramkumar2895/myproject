from fake_useragent import UserAgent  #to randomize the useragent
from bs4 import BeautifulSoup 
from time import strftime  #to convert into otherformat
import urllib.parse
import requests
from html import unescape
from datetime import datetime
import pymysql
import pprint 
import time
import sys
import os
import re

global sess
sess = requests.session()
global count_no
count_no = 1
current_datetime =  datetime.now()
current_month = strftime('%B')
current_date = strftime('%d-%B-%Y')
global cur
connection = pymysql.connect(host='localhost',user='root',password='',db='hk',charset='utf8mb4')
cur = connection.cursor()


def create_Path(ID,Name,Year,Volume,Issue,count_no):
	try:		
		Name = Name.replace(' ','_')
		Name = str(ID)+'_'+str(Name)
		if Volume is not None and Issue is not None:
			V = 'V'+str(Volume)+'N'+str(Issue)
		elif Volume is None and Issue is not None:
			V = 'N'+str(Issue)
		elif Volume is not None and Issue is None:	
			V = 'V'+str(Volume)
		else:
			V = ''		
		PDF_Name = '_'.join(filter(None,[str(ID),Volume,Issue,str(count_no)]))	
		creating_path = os.path.join(os.getcwd(),str(ID),str(Name),str(Year),str(V),str(current_month),str(current_date))			
		if not os.path.exists(creating_path): os.makedirs(creating_path)
		return creating_path,PDF_Name
	except Exception as e:
		print(e)
		return None,None

def write_file(PDF_Link,creating_path,PDF_Name,each):	
	headers = {'content-type': "application/pdf",
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
	'Referer': each}
	r = sess.get(PDF_Link,headers = headers,stream = True,verify = False) 
	file_Name =  str(creating_path)+'\\'+PDF_Name+".pdf"
	with open(file_Name,"wb") as pdf: 
		for chunk in r.iter_content(chunk_size=1024): 	  
			 # writing one chunk at a time to pdf file 
			 if chunk: 
				 pdf.write(chunk) 
	return file_Name			

def get_old_records():
	cur.execute('select Dart_URL,MainLink from car_test1')
	old_records = cur.fetchall()
	return old_records
	
	
	
def check_duplicate_records(Title,each):
	old_records = get_old_records()
	Duplicate = 'No Duplicate'
	for title in old_records:
		Old_title = title[0]
		Each_Link = title[1]		
		if Title is None:Title=''
		if each is None:each=''
		if Old_title.strip() == Title.strip() or Each_Link.strip() == each.strip():
			Duplicate = 'Duplicate'
			break 	
	return Duplicate


def download_PDF(parsedNews,ID,Name,each):
	global count_no
	if parsedNews.get('PDF_URL') is not None:
		PDF_Link = parsedNews.get('PDF_URL')
		newsTitle = parsedNews.get('newsTitle') if parsedNews.get('newsTitle') is not None else ''						
		Volumn = parsedNews.get('PageVolume') if parsedNews.get('PageVolume') is not None else None						
		Issue = parsedNews.get('PageIssue') if parsedNews.get('PageIssue') is not None else None					
		Year = parsedNews.get('Year') if parsedNews.get('Year') is not None else ''									
		creating_path,PDF_Name = create_Path(ID,Name,Year,Volumn,Issue,count_no)
		if creating_path is not None:
			file_Name = write_file(PDF_Link,creating_path,PDF_Name,each)			
			count_no+=1
			return file_Name
	else:
		print('PDF URL not found')
		return 'Failed'



def NoneVerify(data):
	if data == "None":
		return " "
	else:
		return data
		
		
def insert_data(Source_ID=None,D_Vol=None,D_Issu=None,Workflow=None,d_TO_Curl=None,Dart_URL=None,D_Location=None,Pub_Year=None,Pub_Date=None,A_ID=None,artno=None,DOI=None,F_Page=None,L_Page=None,filepath=None,downloadtype =None,MainLink=None,date_format=None,title=None):	
	Source_ID = NoneVerify(Source_ID)
	Pub_Date = dateconvert(Pub_Date)
	D_Vol = NoneVerify(D_Vol)
	D_Issu = NoneVerify(D_Issu)
	Workflow = NoneVerify(Workflow)
	d_TO_Curl = NoneVerify(d_TO_Curl)
	Dart_URL = NoneVerify(Dart_URL)
	D_Location = NoneVerify(D_Location)
	Pub_Year = NoneVerify(Pub_Year)
	Pub_Date = NoneVerify(Pub_Date)
	A_ID = NoneVerify(A_ID)
	artno = NoneVerify(artno)
	DOI = NoneVerify(DOI)
	F_Page = NoneVerify(F_Page)
	L_Page = NoneVerify(L_Page)
	filepath = NoneVerify(filepath)
	downloadtype = NoneVerify(downloadtype)
	MainLink = NoneVerify(MainLink)
	date_format = NoneVerify(date_format)
	title = NoneVerify(title)
	upDOI = reg_exp('(?:https|http)[^>]*?org\/([^>]*?)$',DOI,list=False,strip=True)
	if upDOI == '':
		DOI = DOI 
	else: 
		DOI = upDOI
	DOI = re.sub(r'<[^>]*?>', '', str(DOI))
	cur.execute('INSERT INTO car_test1 (srcid,dvol,diss,workflow,dtocurl,darturl,dlocation,pubyear,pubdate,downdate,aid,artno,doi,fpage,lpage,filepath,downloadtype) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(Source_ID,D_Vol,D_Issu,Workflow,d_TO_Curl,Dart_URL,D_Location,Pub_Year,Pub_Date,date_format,A_ID,artno,DOI,F_Page,L_Page,filepath,downloadtype))
	connection.commit()

def reg_exp(expression, content, list=True, format='',strip=False):
	if expression is not None:
		reList=re.findall(expression,str(content),re.I)
		if reList==[''] or reList==[] :
			data = format
		else:
			if list==False:
				if strip==False: data = str(reList[0])
				else: data = str(reList[0]).strip()
			else:
				if strip==False: data = reList
				else:
					data=[]
					for x in reList: data.append(x.strip())
		return data	


def monthConvert(string):
    m = {
        'jan':'01',
        'feb':'02',
        'mar':'03',
        'apr':'04',
         'may':'05',
         'jun':'06',
         'jul':'07',
         'aug':'08',
         'sep':'09',
         'oct':'10',
         'nov':'11',
         'dec':'12'
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')	
		
def dateconvert(date):
	date = date.strip()
	if len(date) and re.match('[\d]{4}',date)  == 4:
		return date
	elif re.match("[A-z]+\s*[\d]{1,2}\s*(?:\,\s*|\s*)[\d]{4}",date):
		n = re.match("([A-z]+)\s*([\d]{1,2})\s*(?:\,\s*|\s*)([\d]{4})",date)
		mon = n.group(1)
		day = n.group(2)
		Year = n.group(3)
		mon = monthConvert(mon)
		datestr =  Year+"-"+mon+"-"+day
		return datestr
	elif re.match("[\d]{4}\-[\d]{2}\-[\d]{2}",date):
		return date
		
		
	elif re.search("([\d]+(?:\/|\.|\s*)\s*[\d]+(?:\/|\.|\s+)\s*[\d]+)",date):
		datestr = re.sub("\/","-",date)
		datestr = re.sub("\s+","-",datestr)
		datestr = re.sub("\.","-",datestr)
		try:
			datestr = datetime.strptime(datestr, '%d-%m-%Y')
			datestr = datestr.strftime("%Y-%m-%d")
			return datestr
		except:
			datestr = datetime.strptime(datestr, '%Y-%m-%d')
			datestr = datestr.strftime("%Y-%m-%d")
			return datestr	
	elif re.match("([\d]{1,2})\s*([A-z]+)(?:\,\s*|\s*)([\d]{4})",date):
		m= re.match("([\d]{1,2})\s*([A-z]+)(?:\,\s*|\s*)([\d]{4})",date)
		try:
			if len(m.groups()) == 3:
				day = m.group(1)
				mon = m.group(2)
				Year = m.group(3)
				mon = monthConvert(mon)
				datestr =  Year+"-"+mon+"-"+day
				return datestr
		except AttributeError:
			print ("Else Except ::: ",date)
			date = date
			return date
	else:
		return date

def get_old_records():
	cur.execute('select darturl,srcid from car_test1')
	old_records = cur.fetchall()
	return old_records
	
	
def soup_select(cssSelector, content,list=True):
	if cssSelector and content is not None:
		try:
			soup = BeautifulSoup(content,"lxml")
		except:
			soup = content
		data = soup.select(cssSelector)
		if list == True:
			if len(data)>=1:
				return data
			else:
				return None
		else:
			try:
				return data[0]
			except:
				return None
	else:
		return None

	
def GET(url,head=None,contentType='content'):
	cont = sess.get(url,headers = head)
	print("Response Code ::: ",cont.status_code)
	if contentType=='content':
		soup = BeautifulSoup(cont.content,"lxml")
		return soup
	elif contentType==json:
		soup = cont.json()
		return soup

	
def POST(url,head=None,formData=None,contentType='content'):
	cont = sess.post(url,headers = head,data=formData)
	print(cont.status_code)
	if contentType=='content':
		soup = BeautifulSoup(cont.content,"lxml")
		return soup
	elif contentType==json:
		soup = cont.json()
		return soup