from typing import final
from django.http.response import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render
from requests.sessions import session
from selenium import webdriver


# prothom alo
def get_html_content(keywords):
    import requests

    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    
    if keywords:
        keywords = keywords.replace(' ','%20')

        html_content = session.get(f'https://www.prothomalo.com/search?q={keywords}').text
         
    else:
        keywords = ''
        html_content = ''
    
    return html_content

def get_date_news(link):
    import requests
    
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE

    html_content = session.get(f'{link}').text

    return html_content

# the financial express
def get_html_content_new_age(keywords):
    
    
    import requests

    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    if keywords:
        keywords = keywords.replace(' ','+')
        html_content_newage = session.get(f'https://thefinancialexpress.com.bd/search?term=news&query={keywords}').text
        
    else:
        keywords = ''
        html_content_newage = ''        
    
    return html_content_newage

# akashtv24 
def get_html_content_akash(keywords):
    
    
    import requests

    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE

    if keywords:
        keywords = keywords.replace(' ','+')
        
        html_content_jugantor = session.get(f'http://www.akashtv24.com/search?q={keywords}').text
        
    else:
        keywords = ''
        html_content_jugantor = ''        
    
    return html_content_jugantor

# jugantor 

def get_html_content_jugantor_news(keywords):
    # using selenium package with webdriver
    #     
    
    driver = webdriver.Chrome('C:\chromedriver.exe')
    if keywords:
        keywords = keywords.replace(' ','+')

        # any url which is search from google Example are in 
        # (f'https://www.thedailystar.net/search?t={keywords}') ##### => for daily star
        # (f'https://www.jugantor.com/search/google?q={keywords}') ##### => for jugantor

        driver.get(f'https://www.jugantor.com/search/google?q={keywords}') #navigate to the page
        url = driver.execute_script("return document.body.innerHTML") # execute the script from html body tag
        
    else:
        keywords = ''
        url = '' 
    return url

# dmp news
def get_html_content_DMP_news(keywords):
    
    import requests

    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE

    if keywords:
        keywords = keywords.replace(' ','+')
        
        url = session.get(f'https://dmpnews.org/?s={keywords}').text
    else:
        keywords = ''
        url = '' 
    return url
    
def home(request):
        
    divs = None
    linkAndHeader = None
    linkAndHeader2 = None
    linkAndHeader3 = None
    linkAndHeader4 = None
    linkAndHeader5 = None
    if 'keywords' in request.GET:
        
        fromDate = request.GET.get('from')

        toDate = request.GET.get('to')
        
        keywords = request.GET.get('keywords')
        
        # protom alo
        html_content = get_html_content(keywords)
        
        # financial express
        html_content_new_age = get_html_content_new_age(keywords)

        # akash news
        html_content_jugantor = get_html_content_akash(keywords)
        
        #jugantor
        html_content_jug = get_html_content_jugantor_news(keywords)
        
        # dmp news
        html_content_dmp_news = get_html_content_DMP_news(keywords)

        
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html_content, 'html.parser')
        dmp_news = BeautifulSoup(html_content_dmp_news,'html.parser')
        
        # prothom alo all datas
        divs = soup.find_all('div', class_ = 'customStoryCard9-m__base__1rOCp')
        
        allLinks = []
        allHeader = []

        for items in divs:
            
            temp = items.a.text  # Getting Header
            temp2 = items.a.get('href') # Getting Link
            value = get_date_news(temp2)
            
            soup = BeautifulSoup(value, 'html.parser')
            div = soup.find('div', class_ = 'storyPageMetaData-m__publish-time__19bdV storyPageMetaData-m__no-update__3AA06')
            if(div):
                tag = div.time
                attribute = tag['datetime']
            else:                
                attribute = []
            
            
            if(attribute):
                from datetime import timedelta,datetime
                strs = attribute[::-1].replace(':','',1)[::-1]

                try:
                    offset = int(strs[-5:])
                except:
                    print ("Error")

                delta = timedelta(hours = offset / 100)
                time = datetime.strptime(strs[:-5], "%Y-%m-%dT%H:%M:%S")
                time -= delta                
                final_date = time.date()
            else:
                final_date = []

            from datetime import datetime
            if(fromDate):
                date1_obj = datetime.strptime(toDate,'%m/%d/%Y')           
                todate_fin = date1_obj.date()
            else:
                todate_fin = None
            if(fromDate):
                date2_obj = datetime.strptime(fromDate,'%m/%d/%Y')
                fromDate_fin = date2_obj.date()
            else:
                fromDate_fin = None
            
            if(fromDate_fin == None or todate_fin == None):
                allHeader.append([temp])
                allLinks.append([temp2])
            elif((todate_fin >= final_date) and (final_date >= fromDate_fin)):
                allHeader.append([temp])
                allLinks.append([temp2])
            
        # We have two list. So, we will zip them. 
        # First putting header in the zip then link.
        linkAndHeader = zip(allHeader, allLinks)

        # jugantor news paper

        soupForJugantor = BeautifulSoup(html_content_jugantor,'html.parser')
        jugantor = soupForJugantor.find_all('div', class_ = "attachment-block")
        allLinksAkash = []
        allHeaderAkash = []
        for items in jugantor:
            
            temp = items.h4.text  # Getting Header
            
            temp2 = items.a.get('href') # Getting Link
            
            
            # Adding them in list.
            allHeaderAkash.append([temp])
            allLinksAkash.append([temp2])
        linkAndHeader3 = zip(allHeaderAkash,allLinksAkash)

        
        # financial express
        soupForNewAge = BeautifulSoup(html_content_new_age,'html.parser')
        financialExp = soupForNewAge.find_all('div', class_="card row")
        

        allLinksFinanceExp = []
        allHeaderFinanceExp = []

        for items in financialExp:
            
            temp = items.h3.text  # Getting Header
            temp2 = items.p.text # Getting Link
            
            
            # Adding them in list.
            allHeaderFinanceExp.append([temp])
            allLinksFinanceExp.append([temp2])
        
            
        linkAndHeader2 = zip(allHeaderFinanceExp,allLinksFinanceExp)

        # dmp news all
        dmp_news_all = dmp_news.find_all('article', class_ = 'has-post-thumbnail')
        
        allLinksDmp = []
        allHeaderDmp = []

        for dmp in dmp_news_all:
            temp = dmp.h3.text
            temp2 = dmp.h3.a.get('href') # Getting Link
            allHeaderDmp.append([temp])
            allLinksDmp.append([temp2])
        linkAndHeader4 = zip(allHeaderDmp,allLinksDmp)
        
        
        # jugantor news all
        soupForjug = BeautifulSoup(html_content_jug,'html.parser')
        
        jugantor_all = soupForjug.find_all('div', class_ = 'gsc-webResult gsc-result')

        allLinksjugan = []
        allHeaderjugan = []
        for data in jugantor_all:
            temp = data.a.text
            temp2 = data.a.get('href')
            allLinksjugan.append([temp2])
            allHeaderjugan.append([temp])
        linkAndHeader5 = zip(allHeaderjugan,allLinksjugan)
        
    return render(request, 'home.html',{'linkAndHeader': linkAndHeader, 'linkAndHeader2': linkAndHeader2, 'linkAndHeader3':linkAndHeader3,'linkAndHeader4':linkAndHeader4, 'linkAndHeader5': linkAndHeader5})