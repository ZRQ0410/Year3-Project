from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import UrlTable
from .models import Report
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
import requests
import itertools
from collections import Counter
import re
import string

def home(request):
    # each time open the page: check if json files exist
    # if so, read from theses files and pass the data to front end
    try:
        with open('dashboard/data/result_district.json') as f1:
            result_district = json.load(f1)
        with open('dashboard/data/result_overall.json') as f2:
            result_overall = json.load(f2)
    except:
        _analyze_report()

    template = loader.get_template('dashboard/dashboard.html')
    context = {
        'result_district': result_district,
        'result_overall': result_overall,
    }

    return HttpResponse(template.render(context, request))
    # return render(request, 'dashboard/dashboard.html')


def test(request):
    r = Report.objects.filter(start_time='2024-02-25 14:33:48.000000')

    
    template = loader.get_template('dashboard/test.html')
    context = {
        'test': r
    }

    return HttpResponse(template.render(context, request))


def _analyze_district():
    """
    Analyze reports for each district:
        num_evaluated: number of GPs evaluated (same GP names with different postcodes considered as different ones)
        mean_err: average number of errors
        mean_likely: average number of likely problems
        mean_potential: average number of potential problems
        A_percent: percentage of GPs satisfy A level conformance
        AA_percent: percentage of GPs satisfy AA level conformance
        AAA_percent: percentage of GPs satisfy AAA level conformance
    Return:
        {'districtA': {...},
         'districtB': {...},
          ...}
    """
    # get list of unique lad
    lads = UrlTable.objects.exclude(lad__isnull=True).values('lad').distinct()
    districts = [i['lad'] for i in lads]

    result = {}
    for d in districts:
        data = {}
        # for each district: with working url (report_id not null), valid report (num_err not null)
        num_eval = UrlTable.objects.filter(lad=d, report_id__isnull=False, report__num_err__isnull=False).count()
        data['num_evaluated'] = num_eval

        # for all valid reports
        num_err = UrlTable.objects.filter(lad=d, report_id__isnull=False, report__num_err__isnull=False).aggregate(Sum('report__num_err'))['report__num_err__sum']
        num_likely = UrlTable.objects.filter(lad=d, report_id__isnull=False, report__num_err__isnull=False).aggregate(Sum('report__num_likely'))['report__num_likely__sum']
        num_potential = UrlTable.objects.filter(lad=d, report_id__isnull=False, report__num_err__isnull=False).aggregate(Sum('report__num_potential'))['report__num_potential__sum']
        
        data['mean_err'] = num_err / num_eval
        data['mean_likely'] = num_likely / num_eval
        data['mean_potential'] = num_potential / num_eval

        # if a GP satisfies AAA, then it also satisfies A and AA
        num_Alevel = UrlTable.objects.filter(lad=d, report_id__isnull=False, report__num_A=0).count()
        num_AAlevel = UrlTable.objects.filter(lad=d, report_id__isnull=False, report__num_A=0, report__num_AA=0).count()
        num_AAAlevel = UrlTable.objects.filter(lad=d, report_id__isnull=False, report__num_err=0).count()

        data['A_percent'] = num_Alevel / num_eval
        data['AA_percent'] = num_AAlevel / num_eval
        data['AAA_percent'] = num_AAAlevel / num_eval

        result[d] = data
    return result


def _get_top10(lst):
    """
    Given a list of lists, get counts of all values, sort the elements from higher counts to lower counts.
    """
    counts = Counter(itertools.chain.from_iterable(lst)).most_common()
    if len(counts) <= 10:
        return counts
    else:
        return counts[:10]


def _classify_errs():
    """
    Assign each error to its corresponding class: Perceivable, Operable, Understandable, Robust. Compute the number of errors in each class.
    """
    err_query = UrlTable.objects.filter(report_id__isnull=False, report__err__isnull=False).values('report__err')
    err_lst = [e['report__err'] for e in err_query]
    # flatten the list of lists
    err = list(itertools.chain.from_iterable(err_lst))
    with open('dashboard/data/classes.json') as f:
        classes = json.load(f)
        perceive = set(classes['1'])
        operable = set(classes['2'])
        understand = set(classes['3'])
        robust = set(classes['4'])

    err_p, err_o, err_u, err_r = [], [], [], []
    for i in err:
        if i in perceive:
            err_p.append(i)
        elif i in operable:
            err_o.append(i)
        elif i in understand:
            err_u.append(i)
        elif i in robust:
            err_r.append(i)
    return (len(err_p), len(err_o), len(err_u), len(err_r))


def _get_detail(id):
    """
    Get the success criteria, error detail, and short description of the issue.
    """
    res = requests.get("https://websiteaccessibilitychecker.com/checker/suggestion.php?id=" + str(id))
    soup = BeautifulSoup(res.text, 'html')
    sc = soup.find(class_='output-form').find_all('li')[-1].find(class_='padding_left').text
    err = soup.find(class_='output-form').find_all(class_='msg')[4].text
    descr = soup.find(class_='output-form').find_all(class_='msg')[3].text
    return (sc, err, descr)


def _analyze_overall():
    """
    Analyze the overall level:
        num_websites: total number of eval GPs' websites (assume each unique gp has a unique website)
        num_districts: total number of eval districts
        Find top 5 of each class, if less than 5, return all:
            # top_err: most frequent errors
            # top_likely: most frequent likely problems
            # top_potential: most frequent potential problems
            top_A_err: most frequent A level errors
            top_AA_err: most frequent AA level errors
            top_AAA_err: most frequent AAA level errors
        num_p: number of errors in Perceivable class
        num_o: number of errors in Operable class
        num_u: number of errors in Understandable class
        num_r: number of errors in Robust class
        # num_err: total number of errors of all websites
        # num_likely: total number of likely problems
        # num_potential: total number of potential problems
        num_A_err: total number of level A errors
        num_AA_err: total number of level AA errors
        num_AAA_err: total number of level AAA errors
    Return:
        List should be sorted: descending order.
        {'num_websites': num,
         'num_districts': num,
         'top_A_err': [{'id': id1, 'num': num, 'sc': sc, 'msg': issue detail, 'descr': description}, {}, ...],
         'top_AA_err': [...],
         ...}
    """
    result = {}

    result['num_websites'] = UrlTable.objects.filter(report_id__isnull=False, report__num_err__isnull=False).count()
    result['num_districts'] = UrlTable.objects.filter(report_id__isnull=False, report__num_err__isnull=False, lad__isnull=False).values('lad').distinct().count()

    # err_query = UrlTable.objects.filter(report_id__isnull=False, report__err__isnull=False).values('report__err')
    # err = [e['report__err'] for e in err_query]
    # top_err = []
    # err_counts = _get_top10(err)
    # for issue in err_counts:
    #     sc, msg, descr = _get_detail(issue[0])
    #     top_err.append({"id": issue[0], "num": issue[1], "sc": sc, "msg": msg, "descr": descr})
    # result['top_err'] = top_err

    # likely_query = UrlTable.objects.filter(report_id__isnull=False, report__likely__isnull=False).values('report__likely')
    # likely = [l['report__likely'] for l in likely_query]
    # top_likely = []
    # likely_counts = _get_top10(likely)
    # for issue in likely_counts:
    #     sc, msg, descr = _get_detail(issue[0])
    #     top_likely.append({"id": issue[0], "num": issue[1], "sc": sc, "msg": msg, "descr": descr})
    # result['top_likely'] = top_likely

    # potential_query = UrlTable.objects.filter(report_id__isnull=False, report__likely__isnull=False).values('report__potential')
    # potential = [p['report__potential'] for p in potential_query]
    # top_potential = []
    # potential_counts = _get_top10(potential)
    # for issue in potential_counts:
    #     sc, msg, descr = _get_detail(issue[0])
    #     top_potential.append({"id": issue[0], "num": issue[1], "sc": sc, "msg": msg, "descr": descr})
    # result['top_potential'] = top_potential

    err_A_query = UrlTable.objects.filter(report_id__isnull=False, report__err_A__isnull=False).values('report__err_A')
    err_A = [e['report__err_A'] for e in err_A_query]
    top_A_err = []
    err_A_counts = _get_top10(err_A)
    for issue in err_A_counts:
        sc, msg, descr = _get_detail(issue[0])
        top_A_err.append({"id": issue[0], "num": issue[1], "sc": sc, "msg": msg, "descr": descr})
    result['top_A_err'] = top_A_err

    err_AA_query = UrlTable.objects.filter(report_id__isnull=False, report__err_AA__isnull=False).values('report__err_AA')
    err_AA = [e['report__err_AA'] for e in err_AA_query]
    top_AA_err = []
    err_AA_counts = _get_top10(err_AA)
    for issue in err_AA_counts:
        sc, msg, descr = _get_detail(issue[0])
        top_AA_err.append({"id": issue[0], "num": issue[1], "sc": sc, "msg": msg, "descr": descr})
    result['top_AA_err'] = top_AA_err

    err_AAA_query = UrlTable.objects.filter(report_id__isnull=False, report__err_AAA__isnull=False).values('report__err_AAA')
    err_AAA = [e['report__err_AAA'] for e in err_AAA_query]
    top_AAA_err = []
    err_AAA_counts = _get_top10(err_AAA)
    for issue in err_AAA_counts:
        sc, msg, descr = _get_detail(issue[0])
        top_AAA_err.append({"id": issue[0], "num": issue[1], "sc": sc, "msg": msg, "descr": descr})
    result['top_AAA_err'] = top_AAA_err

    result['num_p'], result['num_o'], result['num_u'], result['num_r'] = _classify_errs()

    # result['num_err'] = UrlTable.objects.filter(report_id__isnull=False, report__num_err__isnull=False).aggregate(Sum('report__num_err'))['report__num_err__sum']
    # result['num_likely'] = UrlTable.objects.filter(report_id__isnull=False, report__num_err__isnull=False).aggregate(Sum('report__num_likely'))['report__num_likely__sum']
    # result['num_potential'] = UrlTable.objects.filter(report_id__isnull=False, report__num_err__isnull=False).aggregate(Sum('report__num_potential'))['report__num_potential__sum']

    result['num_A_err'] = UrlTable.objects.filter(report_id__isnull=False, report__num_A__isnull=False).aggregate(Sum('report__num_A'))['report__num_A__sum']
    result['num_AA_err'] = UrlTable.objects.filter(report_id__isnull=False, report__num_A__isnull=False).aggregate(Sum('report__num_AA'))['report__num_AA__sum']
    result['num_AAA_err'] = UrlTable.objects.filter(report_id__isnull=False, report__num_A__isnull=False).aggregate(Sum('report__num_AAA'))['report__num_AAA__sum']

    return result


def _analyze_report():
    """
    Analyze the report in district and overall level.
    Save the reuslts into json files. (under data/)
    """
    # query and anylize data
    # 1. each district
    result_district = _analyze_district()
    # 2. whole level
    result_overall = _analyze_overall()

    # write the results into 2 json files
    with open('dashboard/data/result_district.json', 'w') as f1:
        json.dump(result_district, f1)
    
    with open('dashboard/data/result_overall.json', 'w') as f2:
        json.dump(result_overall, f2)


def districts(request):
    with open('dashboard/data/result_district.json') as f1:
            result_district = json.load(f1)
    with open('dashboard/data/result_overall.json') as f2:
        result_overall = json.load(f2)
    
    template = loader.get_template('dashboard/districts.html')
    context = {
        'result_district': result_district,
        'result_overall': result_overall,
    }
    return HttpResponse(template.render(context, request))


def _url_form(location):
    # strip punctuation
    loc = location.translate(str.maketrans('', '', string.punctuation))
    # replace whitespace with -
    loc = re.sub(r"\s+", '-', loc)
    return loc


def gpdetail_loc(request, letter='A'):
    # get unique locations
    districts = UrlTable.objects.filter(report_id__isnull=False, report__num_err__isnull=False, lad__isnull=False).values('lad').distinct()
    dist = [i['lad'] for i in districts]
    names = sorted([i['lad'] for i in districts if i['lad'].startswith(letter)])
    # urls = [_url_form(i) for i in partial]

    context = {
        'districts': dist,
        # 'name_url': zip(names, urls),
        'names': names,
        'letter': letter
    }
    template = loader.get_template('dashboard/gpdetail.html')
    return HttpResponse(template.render(context, request))


def gpdetail_lad(request, lad):
    evaluated_gps = UrlTable.objects.filter(lad=lad, report_id__isnull=False, report__num_err__isnull=False)
    for gp in evaluated_gps:
        url = gp.url
        if url[-1] == '/':
            gp.url = url[:-1]

    p = Paginator(evaluated_gps, 10)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    page_obj = p.get_page(page_number)

    context = {
        'current_page': int(page_number),
        'page_num': p.num_pages,
        'lad': lad,
        'page_obj': page_obj
    }

    template = loader.get_template('dashboard/gpdetail_lad.html')
    return HttpResponse(template.render(context, request))


def _get_err_detail(err_list, err_info):
    err_detail = []
    for err in Counter(err_list).most_common():
        # [0]: id, [1]: number
        err_id = err[0]
        err_num = err[1]
        sc = err_info[err_id]['sc']
        msg = err_info[err_id]['msg']
        descr = err_info[err_id]['descr']
        err_detail.append({'id': err_id, 'err_num': err_num, 'sc': sc, 'msg': msg, 'descr': descr})
    return err_detail


def gpdetail_report(request, gp_id, report_id):
    gp = UrlTable.objects.filter(id=gp_id)[0]
    report = Report.objects.filter(id=report_id)
    if len(report) == 0:
        return HttpResponse('Page not found.')
    r = report[0]
    
    # get all error detail info
    with open('dashboard/data/err_info.json') as f:
        err_info = json.load(f)
    if r.num_A == 0:
        A_err = []
    else:
        A_err = _get_err_detail(r.err_A, err_info)
    if r.num_AA == 0:
        AA_err = []
    else:
        AA_err = _get_err_detail(r.err_AA, err_info)
    if r.num_AAA == 0:
        AAA_err = []
    else:
        AAA_err = _get_err_detail(r.err_AAA, err_info)

    context = {
        'gp': gp,
        'num_err': r.num_err,
        'num_likely': r.num_likely,
        'num_potential': r.num_potential,
        'num_A': r.num_A,
        'num_AA': r.num_AA,
        'num_AAA': r.num_AAA,
        'A_err': A_err,
        'AA_err': AA_err,
        'AAA_err': AAA_err,
        'update_time': r.start_time
    }
    template = loader.get_template('dashboard/gpdetail_report.html')
    return HttpResponse(template.render(context, request))


def trend(request):
    template = loader.get_template('dashboard/trend.html')
    context = {}
    return HttpResponse(template.render(context, request))


# evaluate all urls periodically
def _achecker_evaluation(current_time):
    """
    Update all data in the Report table.
    Columns in Report table:
        num_err, num_likely, num_potential -> int: number of errors, likely and potential problems 
        err, likely, potential -> [id1, id2, ...], [], []

        num_A, num_AA, num_AAA -> int: number of errors that violate A level sc, AA and AAA level (each level excluded)
        err_A, err_AA, err_AAA -> [id1, id2, ...], [], [] error IDs in A / AA / AAA level
    """
    # get latest report records to insert result
    reports = Report.objects.filter(srart_time=current_time)

    # read 3 levels (A / AA / AAA) of issue IDs from issue_ids.json file (set of strings)
    with open('dashboard/data/issue_ids.json', 'r') as f:
        data = json.load(f)
        A = set(data['A'])
        AA = set(data['AA'])
        AAA = set(data['AAA'])
    
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


# map UrlTable to Report table (update foreign key)
def _url2report(current_time):
    # get all unique working urls
    urls = UrlTable.objects.filter(state=1).values('url').distinct()
    url_lst = [u['url'] for u in urls]

    # put all urls in Report table
    for u in url_lst:
        r = Report(url=u, start_time=current_time)
        r.save()

    # get all objects in url table
    objs = UrlTable.objects.all()
    # match the url in UrlTable with url in Report
    for i in objs:
        if i.url in url_lst:
            r = Report.objects.get(url=i.url, start_time=current_time)
            i.report = r
            i.save()
    

# one-time function to add districts to Url table
# def get_districts(postcode):
#     """
#     Get the local authority district name according to the postcode.
#     If cannot get the district name, set to None.
#     """
#     objs = UrlTable.objects.all()

#     for obj in objs:
#         # postcodes.io api: https://postcodes.io/
#         api = "https://api.postcodes.io/postcodes/" + obj.postcode
#         # get response, if failed, try again
#         for i in range(2):
#             res = requests.get(api).json()
#             if res['status'] == 200:
#                 obj.lad = res['result']['admin_district']
#                 break
#             else:
#                 obj.lad = None
#                 time.sleep(0.5)
#         obj.save()
#     return HttpResponse('Done')