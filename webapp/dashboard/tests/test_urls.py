from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dashboard.views import home, districts, trend, gpdetail_loc, gpdetail_lad, gpdetail_report 

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_districts_url_is_resolved(self):
        url = reverse('districts')
        self.assertEqual(resolve(url).func, districts)
    
    def test_trend_url_is_resolved(self):
        url = reverse('trend')
        self.assertEqual(resolve(url).func, trend)
    
    def test_gpdetail_loc_url_without_args_is_resolved(self):
        url = reverse('gpdetail_loc')
        self.assertEqual(resolve(url).func, gpdetail_loc)

    def test_gpdetail_loc_url_with_args_is_resolved(self):
        url = reverse('gpdetail_loc', args=['Z'])
        self.assertEqual(resolve(url).func, gpdetail_loc)
    
    def test_gp_list_url_is_resolved(self):
        url = reverse('gp_list', args=['someLocation'])
        self.assertEqual(resolve(url).func, gpdetail_lad)
    
    def test_gp_report_url_is_resolved(self):
        url = reverse('gp_report', args=[12, 345])
        self.assertEqual(resolve(url).func, gpdetail_report)
    
   