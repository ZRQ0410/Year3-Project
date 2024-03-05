from django.urls import path
from . import views
from datetime import datetime
import json, logging
from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import register_events, DjangoResultStoreMixin
from django_apscheduler.jobstores import DjangoJobStore, register_job

urlpatterns = [
    path('', views.home),
    path('districts/', views.districts),
    path('trend/', views.trend),
    path('gp-detail/loc/', views.gpdetail_loc, name='gpdetail_loc'),
    path('gp-detail/loc/<str:letter>', views.gpdetail_loc, name='gpdetail_loc'),
    path('gp-detail/lad/<str:lad>', views.gpdetail_lad),
    path('gp-detail/report/<int:gp_id>_<int:report_id>', views.gpdetail_report),
    # path('get_districts/', views.get_districts),
]


scheduler = BackgroundScheduler()
# job stores: default DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")

# execute on the first day of month 1, 4, 7, 10, at 00:00, till 2024-09-01
@register_job(scheduler, 'cron', month='1,4,7,10', day=1, hour=0, minute=0, second=0, end_date='2024-09-01', id='job_eval', replace_existing=True)
def job_eval():
    current_time = datetime.now()
    views._url2report(current_time)
    # evaluate all urls in the database
    views._achecker_evaluation(current_time)
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
