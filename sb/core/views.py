from django.http.response import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render


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

    
def home(request):
    result = None
    divs = None
    if 'keywords' in request.GET:
        
        keywords = request.GET.get('keywords')
        html_content = get_html_content(keywords)

        import re
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html_content, 'html.parser')

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
        print (divs)
        # for items in divs:
        #     result = items.find('h2', class_ = 'headline').text
            

    # return render(request, 'home.html',{'result': result})
    return render(request, 'home.html',{'divs': divs})

