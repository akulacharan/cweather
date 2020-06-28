from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from . import models
from requests.compat import quote_plus

# Create your views here.
url='https://www.timeanddate.com/weather/india/{}'
BASE_IMAGE_URL='https://c.tadst.com/gfx/w/svg/wt-{}.svg'

def home(request):
    return render(request,'base.html')


def search(request,model=None):
    search = request.POST.get('search')
    models.search.objects.create(search=search)
    final_url = url.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('div', {'id': 'qlook'})

    final_postings = []

    for post in post_listings:
        present = post.find(class_='h1').get_text()
        degree = post.find(class_='h2').get_text()
        covering = post.find('p').get_text()
        forcast = post.find('span').get_text()
        img = post.find(class_='mtt').get('src').split('-')[1].split('.')[0]
        image = BASE_IMAGE_URL.format(img)

        final_postings.append((present, degree, covering, forcast, image))
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings
    }

    return render(request,'main/index.html',stuff_for_frontend)

