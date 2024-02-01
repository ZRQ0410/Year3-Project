# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import UrlTable
from .models import Report
import requests
from bs4 import BeautifulSoup
import time
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
# def url2report(request):
#     # get all unique working urls
#     urls = UrlTable.objects.filter(state=1).values('url').distinct()
#     url_lst = [u['url'] for u in urls]

#     # put all urls in Report table
#     for u in url_lst:
#         r = Report(url=u)
#         r.save()

#     # get all objects in url table
#     objs = UrlTable.objects.all()
#     # match the url in UrlTable with url in Report
#     for i in objs:
#         if i.url in url_lst:
#             r = Report.objects.get(url=i.url)
#             i.report = r
#             i.save()
    
#     return HttpResponse('Done')
    

def test(request):
    return HttpResponse('Test page')


def achecker_evaluation(request):
    """
    Update all data in the Report table.
    Columns in Report table:
        num_err, num_likely, num_potential -> int: number of errors, likely and potential problems 
        err, likely, potential -> [id1, id2, ...], [], []

        num_A, num_AA, num_AAA -> int: number of errors that violate A level sc, AA and AAA level (each level excluded)
        err_A, err_AA, err_AAA -> [id1, id2, ...], [], [] error IDs in A / AA / AAA level
    """
    reports = Report.objects.all()

    # read 3 levels (A / AA / AAA) of issue IDs from issue_id.txt file (set of strings)
    with open('issue_ids.txt', 'r') as f:
        # print(set(map(int, f.readlines()[0].split(','))))
        levels = f.read().split('\n')
        A = set(levels[0].split(','))
        AA = set(levels[1].split(','))
        AAA = set(levels[2].split(','))
    
    # evaluate each url and store the report
    for report in reports:
        url = 'https://websiteaccessibilitychecker.com/checkacc.php?uri='+report.url+'&%20id=b0a02df9fec9f65d0da2fc658b3b393fc689a3eb&output=html&guide=WCAG2-AAA'
        res = requests.get(url)
        time.sleep(0.2)
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # if status is not 200, do not update data
            continue

        # parse the result
        soup = BeautifulSoup(res.text, 'html')

        errors = soup.find(id='errors')
        likely_probs = soup.find(id='likely_problems')
        potential_probs = soup.find(id='potential_problems')

        if errors is not None:
            err_msgs = errors.find_all(class_='msg')
            num_err = len(err_msgs)
            err = []
            # get the issue id
            for i in err_msgs:
                err.append(i.find('a')['href'].split("id=", 1)[1])
            
            # divide errors into A / AA / AAA level
            err_A = [i for i in err if i in A]
            err_AA = [i for i in err if i in AA]
            err_AAA = [i for i in err if i in AAA]

            # number of errors in level A / AA / AAA
            num_A = len(err_A)
            num_AA = len(err_AA)
            num_AAA = len(err_AAA)

            if num_A == 0:
                err_A = None
            if num_AA == 0:
                err_AA = None
            if num_AAA == 0:
                err_AAA = None

        # if no errors found
        else:
            num_err = 0
            num_A = 0
            num_AA = 0
            num_AAA = 0
            err = None
            err_A = None
            err_AA = None
            err_AAA = None

        if likely_probs is not None:
            likely_msgs = likely_probs.find_all(class_='msg')
            num_likely = len(likely_msgs)
            likely = []
            for i in likely_msgs:
                likely.append(i.find('a')['href'].split("id=", 1)[1])
        else:
            num_likely = 0
            likely = None

        if potential_probs is not None:
            potential_msgs = potential_probs.find_all(class_='msg')
            num_potential = len(potential_msgs)
            potential = []
            for i in potential_msgs:
                potential.append(i.find('a')['href'].split("id=", 1)[1])
        else:
            num_potential = 0
            potential = None

        report.num_err = num_err # number of errors
        report.num_likely = num_likely # number of likely problems
        report.num_potential = num_potential # number of potential problems
        report.err = err # issue id for errors (json)
        report.likely = likely # issue id for likely problems (json)
        report.potential = potential # issue id for potential problems (json)
        report.num_A = num_A # number of errors at A level
        report.num_AA = num_AA # number of errors at AA level
        report.num_AAA = num_AAA # number of errors at AAA level
        report.err_A = err_A # issue id for A level error (json)
        report.err_AA = err_AA # issue id for AA level error (json)
        report.err_AAA = err_AAA # issue id for AAA level error (json)

        # save updated report object
        report.save()
    
    return HttpResponse('Done')



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
