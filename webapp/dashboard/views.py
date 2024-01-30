# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import UrlTable
from .models import Report

import requests

def home(request):
    # urls = UrlTable.objects.exclude(url__isnull=True)
    urls = UrlTable.objects.filter(state=1).values('url').distinct()

    template = loader.get_template('dashboard/dashboard.html')
    context = {
        'num_of_urls': len(urls),
        'urls': urls[:100],
    }

    return HttpResponse(template.render(context, request))
    # return render(request, 'dashboard/dashboard.html')


# one time function to map UrlTable to Report table (add foreign key)
def url2report(request):
    # get all unique working urls
    urls = UrlTable.objects.filter(state=1).values('url').distinct()
    url_lst = [u['url'] for u in urls]

    # put all urls in Report table
    for u in url_lst:
        r = Report(url=u)
        r.save()

    # get all objects in url table
    objs = UrlTable.objects.all()
    # match the url in UrlTable with url in Report
    for i in objs:
        if i.url in url_lst:
            r = Report.objects.get(url=i.url)
            i.report = r
            i.save()
    
    return HttpResponse('Done')
    

def other(request):
    return HttpResponse('Other pages')


def achecker_evaluation(request):
    # get all unique working urls
    urls = UrlTable.objects.filter(state=1).values('url').distinct()
    url_lst = [u['url'] for u in urls]

    for url in url_lst:
    
    
        xml = requests.get(url)
        # tree = ET.parse(xml)
        # root = tree.getroot()

        # return HttpResponse(f'{root.tag}')

        # data = res.json()[0]
        # return HttpResponse(res)






# UnicodeDecodeError: 'gbk' codec can't decode byte 0xa6 in position 37359: illegal multibyte sequence
# def axe(request):
#     from playwright.sync_api import sync_playwright
#     from axe_core_python.sync_playwright import Axe

#     axe = Axe()

#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch()
#         page = browser.new_page()
#         page.goto("https://berrylanemedicalcentre.co.uk")
#         result = axe.run(page)
#         browser.close()

#     violations = result['violations']
#     return HttpResponse("{} violations found.".format(len(violations)))
