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
        # print(html_content)
        
    else:
        keywords = ''
        html_content = ''        
    
    return html_content

# new age paper
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
    result = None
    divs = None
    linkAndHeader = None
    # linkAndHeaderNews = None
    if 'keywords' in request.GET:
        
        keywords = request.GET.get('keywords')
        # protom alo
        html_content = get_html_content(keywords)
        
        # new age
        html_content_new_age = get_html_content_new_age(keywords)
        
        import re
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html_content, 'html.parser')
        # newsage
        soupForNewAge = BeautifulSoup(html_content_new_age,'html.parser')
        
        # single data
        # if keywords:
        #     result = dict()
            
        #     linkValue = soup.find('a', attrs={'href': re.compile("^https://")})
            
        #     result['link'] = str(linkValue.attrs['href']) + "\n"
        #     # result['link'] = soup.find()

        #     result['title'] = soup.find('h2', class_ = 'headline').text
        # else:
        #     result = None      



        # all datas
        divs = soup.find_all('div', class_ = 'customStoryCard9-m__base__1rOCp')
        
        # print(divs)
        # print (divsNewAge)
        # for items in divs:
        #     result = items.find('h2', class_ = 'headline').text
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

        
        
    # return render(request, 'home.html',{'result': result})
    # return render(request, 'home.html',{'divs': divs})
    return render(request, 'home.html',{'linkAndHeader': linkAndHeader})


