from django.urls import path
from . import views
import datetime, json, logging
from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import register_events, DjangoResultStoreMixin
from django_apscheduler.jobstores import DjangoJobStore, register_job

urlpatterns = [
    path('', views.home),
    path('districts/', views.districts),
    path('test/', views.test),
    # path('achecker_evaluation/', views.achecker_evaluation),
    # path('url2report/', views.url2report),
    # path('get_districts/', views.get_districts),
]


scheduler = BackgroundScheduler()
# job stores: default DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")

# @register_job(scheduler, "interval", seconds=60, id='test_job2')
# execute on the first day of month 1, 4, 7, 10, at 00:00, till 2024-09-01
@register_job(scheduler, 'cron', month='1,4,7,10', day=1, hour=0, minute=0, second=0, end_date='2024-09-01', id='job_eval', replace_existing=True)
def job_eval():
    # evaluate all urls in the database
    views._achecker_evaluation()
    # analyze the results
    result_district = views._analyze_district()
    result_overall = views._analyze_overall()
    # write to new json file
    current_time = str(datetime.datetime.now().date())
    try:
        filename = 'dashboard/data/result_district_' + current_time + '.json'
        with open(filename, 'w') as f1:
                json.dump(result_district, f1)
    except Exception:
        logging.exception("An exception was thrown.")
    try:
        filename = 'dashboard/data/result_overall_' + current_time + '.json'
        with open(filename, 'w') as f2:
                json.dump(result_overall, f2)
    except Exception:
        logging.exception("An exception was thrown.")
    # print('run scheduler')

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
