from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import UrlTable, Report
from dashboard.views import _analyze_district, _analyze_overall, _get_top10
import requests

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
            num_err = 5,
            num_likely = 10,
            num_potential = 20,
            num_A = 1,
            num_AA = 1,
            num_AAA = 3,
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
    
    def test_achecker_api_response(self):
        url = 'https://websiteaccessibilitychecker.com/checkacc.php?uri='+'https://www.djangoproject.com/'+'&%20id=b0a02df9fec9f65d0da2fc658b3b393fc689a3eb&output=html&guide=WCAG2-AAA'
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)

    def test_postcode_api_response(self):
        url = "https://api.postcodes.io/postcodes/" + 'm156pf'
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['result']['admin_district'], 'Manchester')
    
    def test_analyze_district(self):
        result = _analyze_district()
        data = {'Manchester': {'num_evaluated': 1, 'mean_err': 5.0, 'mean_likely': 10.0, 'mean_potential': 20.0, 'A_percent': 0.0, 'AA_percent': 0.0, 'AAA_percent': 0.0}}
        self.assertEqual(result, data)

    def test_analyze_overall(self):
        result = _analyze_overall()
        data = {'num_websites': 1, 'num_districts': 1, 'top_A_err': [], 'top_AA_err': [], 'top_AAA_err': [], 'num_p': 0, 'num_o': 0, 'num_u': 0, 'num_r': 0, 'num_A_err': 1, 'num_AA_err': 1, 'num_AAA_err': 3}
        self.assertEqual(result, data)

