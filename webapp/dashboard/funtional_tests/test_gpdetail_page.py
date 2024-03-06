from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from dashboard.models import UrlTable, Report

class TestHomePage(StaticLiveServerTestCase):

    # run once before all tests
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()
        

    @classmethod
    def tearDownClass(cls):
        super().setUpClass()
        cls.browser.close()

    def test_user_sees_map(self):
        self.browser.get(self.live_server_url + reverse('gpdetail_loc'))
        plot = self.browser.find_element(By.ID, 'lad-map').get_attribute("innerHTML")
        self.assertIn('<canvas', plot)
    
    def test_user_sees_location_list(self):
        report = Report.objects.create(
            id = 1,
            url = 'report1.com',
            num_err = 2
        )
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp1',
            url = 'report1.com',
            report = report,
            lad = 'Manchester'
        )
        self.browser.get(self.live_server_url + reverse('gpdetail_loc'))
        # location 'Manchester' name should not appear in default page
        self.assertEquals(
            self.browser.find_element(By.CLASS_NAME, 'partial-districts').text,
            ''
        )
        # should appear under list 'M'
        self.browser.get(self.live_server_url + reverse('gpdetail_loc', args=['M']))
        self.assertEquals(
            self.browser.find_element(By.CLASS_NAME, 'partial-districts').find_element(By.TAG_NAME, 'li').text,
            'Manchester'
        )
    
    def test_search_redirects_to_search_reuslts(self):
        report1 = Report.objects.create(
            id = 1,
            url = 'report1.com',
            num_err = 2
        )
        report2 = Report.objects.create(
            id = 2,
            url = 'report2.com',
            num_err = 5
        )
        urlTable1 = UrlTable.objects.create(
            id = 1,
            gp = 'gp1',
            url = 'report1.com',
            report = report1,
            lad = 'Manchester'
        )
        urlTable2 = UrlTable.objects.create(
            id = 2,
            gp = 'gp2',
            url = 'report2.com',
            report = report2,
            lad = 'Adur'
        )
        self.browser.get(self.live_server_url + reverse('gpdetail_loc'))
        self.browser.find_element(By.TAG_NAME, 'input').send_keys('manchester')
        self.browser.find_element(By.TAG_NAME, 'button').click()
        redirect_url = self.live_server_url + reverse('gpdetail_loc') + '?search=manchester'
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
        # should only display the only gp in Manchester
        self.browser.get(self.live_server_url + reverse('gpdetail_loc') + '?search=manchester')
        self.assertEquals(
            len(self.browser.find_elements(By.CLASS_NAME, 'gp-name')),
            1
        )
        self.assertEquals(
            self.browser.find_element(By.CLASS_NAME, 'gp-name').find_element(By.TAG_NAME, 'a').text,
            'gp1'
        )

    def test_analysis_button_redirects_to_home_page(self):
        self.browser.get(self.live_server_url + reverse('gpdetail_loc'))
        redirect_url = self.live_server_url + reverse('home')
        self.browser.find_element(By.CLASS_NAME, 'side-bar').find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_overall_button_redirects_to_home_page(self):
        self.browser.get(self.live_server_url + reverse('gpdetail_loc'))
        redirect_url = self.live_server_url + reverse('home')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[0].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_district_button_redirects_to_districts_page(self):
        self.browser.get(self.live_server_url + reverse('gpdetail_loc'))
        redirect_url = self.live_server_url + reverse('districts')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[1].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_trend_button_redirects_to_trend_page(self):
        self.browser.get(self.live_server_url + reverse('gpdetail_loc'))
        redirect_url = self.live_server_url + reverse('trend')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[2].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_gpdetail_button_redirects_to_gp_page(self):
        self.browser.get(self.live_server_url + reverse('gpdetail_loc'))
        redirect_url = self.live_server_url + reverse('gpdetail_loc')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[3].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )