from bs4 import BeautifulSoup
import requests
import html5lib
import re
import lxml
import html
import json
import urllib.request

sec = requests.Session()

def clean(text):
    text = re.sub(r'<style[^>]*?>[\w\W]*?<\/style>',' ',str(text))
    text = re.sub(r'<(?!img).*?>',' ',str(text))
    text = re.sub(r'\s+', ' ', str(text))
    text = re.sub(r'^\s*', '', str(text))
    text = re.sub(r'\s*$', '', str(text))
    text = re.sub(r'\s+\s+', ' ', str(text))
    text = re.sub(r'\t', '', str(text))
    return html.unescape(text).strip()

def clean2(text):
    text = re.sub(r'<style[^>]*?>[\w\W]*?<\/style>',' ',str(text))
    text = re.sub(r'<[^>]*?>',' ',str(text))
    text = re.sub(r'\s+', ' ', str(text))
    text = re.sub(r'^\s*', '', str(text))
    text = re.sub(r'\s*$', '', str(text))
    text = re.sub(r'\s+\s+', ' ', str(text))
    text = re.sub(r'\t', '', str(text))
    text = re.sub(r'"', '\\"', str(text))
    return html.unescape(text).strip()

def urlClean(text):
    text = re.sub(r'\\','',str(text))
    return text

def processRegex(regex,content):
	reList=re.findall(regex,content,re.IGNORECASE)
	if reList==[''] or reList==[]:
		return ''
	else:
		return reList[0]

def dataWritter(content, mainContent):
    productTitle = content.get("title", "")
    print(productTitle)
    brand_name = mainContent.get("brand_name", [])
    if brand_name != []:
        brand_name = brand_name[0]
    else:
        brand_name = ""
    print(brand_name)
    variant_name = content.get("variant_name", "")
    productDescription = clean(content.get('description', ""))

    pd = re.findall(r'src\=\"([^>]*?)\"',str(productDescription),re.I)
    if len(pd) >= 10:
	    pd = (pd[0:10])
    else:
        s = 10 - len(pd)
        for i in range(s):
	        pd.append("")

    pd_img_Link1 = pd[0]
    pd_img_Link2 = pd[1]
    pd_img_Link3 = pd[2]
    pd_img_Link4 = pd[3]
    pd_img_Link5 = pd[4]
    pd_img_Link6 = pd[5]
    pd_img_Link7 = pd[6]
    pd_img_Link8 = pd[7]
    pd_img_Link9 = pd[8]
    pd_img_Link10 = pd[9]

    productDescriptionTextOnly = clean2(productDescription)
    productId = content.get('product_id', "")
    productPrice = content.get('price', "")
    productStockStatus = content.get('in_stock', "")

    if productStockStatus == True:
        productStatus = "In Stock"
    else:
        productStatus = "Out Of Stock"
    productMRP = content.get('mrp', "")
    productStarRating = mainContent.get('star_rating', "")
    productStartRatingCount = mainContent.get('star_rating_count', "")
    productExpireDate = content.get('expdt', "")
    productSize = content.get('pack_size', "")
    productDiscount = content.get('discount', "")
    productMedia = content.get('media', [])
    productMediaUrl = ([ x.get('url') for x in productMedia ])
    if len(productMediaUrl) >= 10:
	    productMediaUrl = (productMediaUrl[0:10])
    else:
        n = 10 - len(productMediaUrl)
        for j in range(n):
	        productMediaUrl.append("")
    
    productMediaUrl1 = productMediaUrl[0]
    productMediaUrl2 = productMediaUrl[1]
    productMediaUrl3 = productMediaUrl[2]
    productMediaUrl4 = productMediaUrl[3]
    productMediaUrl5 = productMediaUrl[4]
    productMediaUrl6 = productMediaUrl[5]
    productMediaUrl7 = productMediaUrl[6]
    productMediaUrl8 = productMediaUrl[7]
    productMediaUrl9 = productMediaUrl[8]
    productMediaUrl10 = productMediaUrl[9]

    productImageUrl = content.get('imageUrl', "")
    countryOfOrgin = mainContent.get('originOfCountryName', "")
    countryOfManufacture = mainContent.get('countryOfManufacture', "")
    productIngredients = content.get('product_ingredients', "")
    productUsage = content.get('how_to_use', "")

    with open('C:\\Users\\Administrator\\Desktop\\Nykaa\\Output.txt', 'a', encoding = 'utf-8') as OP:
        OP.write(f'{brand_name}\t{productTitle}\t{variant_name}\t{productStatus}\t{productSize}\t{pd_img_Link1}\t{pd_img_Link2}\t{pd_img_Link3}\t{pd_img_Link4}\t{pd_img_Link5}\t{pd_img_Link6}\t{pd_img_Link7}\t{pd_img_Link8}\t{pd_img_Link9}\t{pd_img_Link10}\t{productDescriptionTextOnly}\t{productId}\t{productPrice}\t{productMRP}\t{productDiscount}\t{productStarRating}\t{productStartRatingCount}\t{productExpireDate}\t{countryOfOrgin}\t{countryOfManufacture}\t{clean(productIngredients)}\t{clean(productUsage)}\t{productMediaUrl1}\t{productMediaUrl2}\t{productMediaUrl3}\t{productMediaUrl4}\t{productMediaUrl5}\t{productMediaUrl6}\t{productMediaUrl7}\t{productMediaUrl8}\t{productMediaUrl9}\t{productMediaUrl10}\t{productImageUrl}\n')



def dataExtraction(content):
    mainDataJsonString = processRegex(r'__PRELOADED_STATE__\s*\=\s*(.*)', str(content))
    mainDataJson = json.loads(mainDataJsonString)
    productDetailJson = mainDataJson.get('productReducer').get('product')
    multipleShades = productDetailJson.get('options')
    with open (f'mypageContent.html','w',encoding = 'utf-8') as f:
        f.write(str(productDetailJson))
    if multipleShades:
        for option in multipleShades:
            dataWritter(option, productDetailJson)
    else:
        print('=================================================')
        dataWritter(productDetailJson, productDetailJson)

with open('C:\\Users\\Administrator\\Desktop\\Nykaa\\Output.txt', 'w', encoding = 'utf-8') as OP:
    OP.write("Brand Name\tProduct Name\tvariant_name\tStock Status\tProduct quantity\tProduct image1\tProduct image2\tProduct image3\tProduct image4\tProduct image5\tProduct image6\tProduct image7\tProduct image8\tProduct image9\tProduct image10\tDescription without tags\tProduct ID\tProduct current price\tProduct MRP\tProduct Discount\tProduct Rating\tProduct Rating Count\tProduct Expire date\tCountry Of Orgin\tCountryOf Manufacture\tIngredients\tHow to use\tProduct Image url1\tProduct Image url2\tProduct Image url3\tProduct Image url4\tProduct Image url5\tProduct Image url6\tProduct Image url7\tProduct Image url8\tProduct Image url9\tProduct Image url10\tProduct Icon\n")
with open('C:\\Users\\Administrator\\Desktop\\Nykaa\\input1.txt','r',encoding = 'utf-8') as f:
    for urls in f:
        pagenationLink = urls.strip()
        pagenationPing = sec.get(str(pagenationLink.strip()))
        pagenationUrlStatus = pagenationPing.status_code
        print(f'Page Status:  {pagenationUrlStatus}')
        if pagenationUrlStatus == 200: 
            pagenationContent = pagenationPing.json().get("response")
    
            if pagenationContent:
                products = pagenationContent.get('products', "")
                for product in products:
                    productUrl = product.get('product_url')
                    if productUrl:
                        productPagePing = sec.get(productUrl)
                        productUrlStatus = productPagePing.status_code
                        print(f'Site Status:  {productUrlStatus}')
                        if productUrlStatus == 200:
                            productPageContent = BeautifulSoup(productPagePing.content,'html5lib')
                            dataExtraction(productPageContent)
                        else:
                            with open('unprocessedProductUrl.txt','a',encoding = 'utf-8')as m:
                                m.write(f'{productUrl}\n')
        else:
            with open('unprocessedPageNationUrl.txt','a',encoding = 'utf-8')as n:
                n.write(f'{pagenationLink}\n')
