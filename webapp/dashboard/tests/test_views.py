from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import UrlTable, Report

class TestViews(TestCase):

    # run before other tests
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.districts_url = reverse('districts')
        self.trend_url = reverse('trend')
        self.loc_url = reverse('gpdetail_loc')
        self.loc_url_withargs = reverse('gpdetail_loc', args=['L'])
        self.report1 = Report.objects.create(
            id = 1,
            url = 'report1.com',
            num_err = 5
        )
        self.report2 = Report.objects.create(
            id = 2,
            url = 'report2.com',
            num_err = 2
        )
        self.urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp1',
            url = 'report1.com',
            report = self.report1,
            lad = 'Manchester'
        )

    def test_home_function(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')
    
    def test_districs_function(self):
        response = self.client.get(self.districts_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/districts.html')
    
    def test_trend_function(self):
        response = self.client.get(self.trend_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/trend.html')
    
    def test_gpdetail_loc_function_without_args(self):
        response = self.client.get(self.loc_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/gpdetail.html')

    def test_gpdetail_loc_function_with_correct_letter(self):
        url = reverse('gpdetail_loc', args=['A'])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/gpdetail.html')

    def test_gpdetail_loc_function_with_incorrect_letter(self):
        url = reverse('gpdetail_loc', args=['3'])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'dashboard/gpdetail.html')
    
    def test_search_function_with_empty_string(self):
        response = self.client.get(self.loc_url, {'search': ''})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/gpdetail.html')
    
    def test_search_function_with_other_string(self):
        response = self.client.get(self.loc_url, {'search': 'Some other search'})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/gpdetail_search.html')

    def test_gpdetail_lad_function_with_correct_lad_name(self):
        url = reverse('gp_list', args=['Manchester'])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/gpdetail_lad.html')

    def test_gpdetail_lad_function_with_incorrect_lad_name(self):
        url = reverse('gp_list', args=['WrongPlaceName'])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'dashboard/gpdetail_lad.html')
    
    def test_gpdetail_report_function_with_correct_args(self):
        url = reverse('gp_report', args=[self.urlTable.report.id, self.report1.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/gpdetail_report.html')
    
    def test_gpdetail_report_function_with_incorrect_args(self):
        url = reverse('gp_report', args=[self.urlTable.report.id, self.report2.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'dashboard/gpdetail_report.html')