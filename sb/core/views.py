from django.http.response import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render

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
    
def home(request):
    # import datetime
    # stime = "09/21/2021 00:00:00.0000"
    
    # print(int(datetime.datetime.strptime(stime, '%m/%d/%Y %H:%M:%S.%f').timestamp()))
    # 1632160800
    # 
    result = None
    divs = None
    linkAndHeader = None
    linkAndHeader2 = None
    
    if 'keywords' in request.GET:
        
        keywords = request.GET.get('keywords')
        # protom alo
        html_content = get_html_content(keywords)
        
        # financial express
        html_content_new_age = get_html_content_new_age(keywords)
        
        import re
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html_content, 'html.parser')
        
        
        # prothom alo all datas
        divs = soup.find_all('div', class_ = 'customStoryCard9-m__base__1rOCp')
        
        allLinks = []
        allHeader = []

        for items in divs:
            temp = items.a.text  # Getting Header
            temp2 = items.a.get('href') # Getting Link
            
            # Adding them in list.
            allHeader.append([temp])
            allLinks.append([temp2])
            
        # We have two list. So, we will zip them. 
        # First putting header in the zip then link.
        linkAndHeader = zip(allHeader, allLinks)
        
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
            
        # We have two list. So, we will zip them. 
        # First putting header in the zip then link.
        linkAndHeader2 = zip(allHeaderFinanceExp,allLinksFinanceExp)
        
    return render(request, 'home.html',{'linkAndHeader': linkAndHeader, 'linkAndHeader2': linkAndHeader2})