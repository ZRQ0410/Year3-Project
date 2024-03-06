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

    def test_user_sees_err_number_cards(self):
        report = Report.objects.create(
            id = 1,
            url = 'report.com',
            num_err = 0,
            num_likely = 0,
            num_potential = 0,
            num_A = 0,
            num_AA = 0,
            num_AAA = 0
        )
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp',
            url = 'report.com',
            report = report,
            lad = 'Manchester'
        )
        self.browser.get(self.live_server_url + reverse('gp_report', args=[1, 1]))
        labels = self.browser.find_elements(By.CLASS_NAME, 'data-label')
        self.assertEquals(
            labels[0].text,
            "Errors"
        )
        self.assertEquals(
            labels[1].text,
            "Likely Problems"
        )
        self.assertEquals(
            labels[2].text,
            "Potential Problems"
        )
        self.assertEquals(
            labels[3].text,
            "A Level Errors"
        )
        self.assertEquals(
            labels[4].text,
            "AA Level Errors"
        )
        self.assertEquals(
            labels[5].text,
            "AAA Level Errors"
        )
       
    def test_zero_errors_and_zero_problems(self):
        report = Report.objects.create(
            id = 1,
            url = 'report.com',
            num_err = 0,
            num_likely = 0,
            num_potential = 0,
            num_A = 0,
            num_AA = 0,
            num_AAA = 0
        )
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp',
            url = 'report.com',
            report = report,
            lad = 'Manchester'
        )
        self.browser.get(self.live_server_url + reverse('gp_report', args=[1, 1]))
        html = self.browser.find_element(By.TAG_NAME, 'main').get_attribute("innerHTML")
        # should not display bar plot
        self.assertNotIn('<div class="card report-bar">', html)
        # should not display error list
        self.assertNotIn('<div class="card err-table">', html)
    
    def test_nonzero_errors_and_nonzero_problems(self):
        report = Report.objects.create(
            id = 1,
            url = 'report.com',
            num_err = 6,
            num_likely = 10,
            num_potential = 20,
            num_A = 1,
            num_AA = 2,
            num_AAA = 3
        )
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp',
            url = 'report.com',
            report = report,
            lad = 'Adur'
        )
        self.browser.get(self.live_server_url + reverse('gp_report', args=[1, 1]))
        html = self.browser.find_element(By.TAG_NAME, 'main').get_attribute("innerHTML")
        # should display bar plot
        self.assertIn('<div class="card report-bar">', html)
        self.assertIn('<canvas', html)
        # should display error list
        self.assertIn('<div class="card err-table">', html)
    
    def test_nonzero_errors_with_zero_AAAerr(self):
        report = Report.objects.create(
            id = 1,
            url = 'report.com',
            num_err = 2,
            num_likely = 10,
            num_potential = 20,
            num_A = 1,
            num_AA = 1,
            num_AAA = 0,
        )
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp',
            url = 'report.com',
            report = report,
            lad = 'Birmingham'
        )
        self.browser.get(self.live_server_url + reverse('gp_report', args=[1, 1]))
        html = self.browser.find_element(By.TAG_NAME, 'main').get_attribute("innerHTML")
        # should display bar plot
        self.assertIn('<div class="card report-bar">', html)
        self.assertIn('<canvas', html)
        # should display error list
        self.assertIn('<div class="card err-table">', html)
        # should not display 'no error message' for A and AA
        self.assertNotIn(
            'No A level errors',
            self.browser.find_element(By.ID, 'no-A-msg').get_attribute("innerHTML")
        )
        self.assertNotIn(
            'No AA level errors',
            self.browser.find_element(By.ID, 'no-AA-msg').get_attribute("innerHTML")
        )
        # should display 'no error message' for AAA
        self.assertIn(
            'No AAA level errors',
            self.browser.find_element(By.ID, 'no-AAA-msg').get_attribute("innerHTML")
        )

    def test_analysis_button_redirects_to_home_page(self):
        report = Report.objects.create(
            id = 1,
            url = 'report.com',
            num_err = 2,
            num_likely = 10,
            num_potential = 20,
            num_A = 1,
            num_AA = 1,
            num_AAA = 0,
        )
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp',
            url = 'report.com',
            report = report,
            lad = 'Birmingham'
        )
        self.browser.get(self.live_server_url + reverse('gp_report', args=[1, 1]))
        redirect_url = self.live_server_url + reverse('home')
        self.browser.find_element(By.CLASS_NAME, 'side-bar').find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_overall_button_redirects_to_home_page(self):
        report = Report.objects.create(
            id = 1,
            url = 'report.com',
            num_err = 2,
            num_likely = 10,
            num_potential = 20,
            num_A = 1,
            num_AA = 1,
            num_AAA = 0,
        )
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp',
            url = 'report.com',
            report = report,
            lad = 'Birmingham'
        )
        self.browser.get(self.live_server_url + reverse('gp_report', args=[1, 1]))
        redirect_url = self.live_server_url + reverse('home')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[0].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_district_button_redirects_to_district_page(self):
        report = Report.objects.create(
            id = 1,
            url = 'report.com',
            num_err = 2,
            num_likely = 10,
            num_potential = 20,
            num_A = 1,
            num_AA = 1,
            num_AAA = 0,
        )
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp',
            url = 'report.com',
            report = report,
            lad = 'Birmingham'
        )
        self.browser.get(self.live_server_url + reverse('gp_report', args=[1, 1]))
        redirect_url = self.live_server_url + reverse('districts')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[1].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_trend_button_redirects_to_trend_page(self):
        report = Report.objects.create(
            id = 1,
            url = 'report.com',
            num_err = 2,
            num_likely = 10,
            num_potential = 20,
            num_A = 1,
            num_AA = 1,
            num_AAA = 0,
        )
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp',
            url = 'report.com',
            report = report,
            lad = 'Birmingham'
        )
        self.browser.get(self.live_server_url + reverse('gp_report', args=[1, 1]))
        redirect_url = self.live_server_url + reverse('trend')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[2].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_gpdetail_button_redirects_to_gp_page(self):
        report = Report.objects.create(
            id = 1,
            url = 'report.com',
            num_err = 2,
            num_likely = 10,
            num_potential = 20,
            num_A = 1,
            num_AA = 1,
            num_AAA = 0,
        )
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp',
            url = 'report.com',
            report = report,
            lad = 'Birmingham'
        )
        self.browser.get(self.live_server_url + reverse('gp_report', args=[1, 1]))
        redirect_url = self.live_server_url + reverse('gpdetail_loc')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[3].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_gpdetail_horizontal_bar_redirects_to_gp_page(self):
        report = Report.objects.create(
            id = 1,
            url = 'report.com',
            num_err = 2,
            num_likely = 10,
            num_potential = 20,
            num_A = 1,
            num_AA = 1,
            num_AAA = 0,
        )
        urlTable = UrlTable.objects.create(
            id = 1,
            gp = 'gp',
            url = 'report.com',
            report = report,
            lad = 'Birmingham'
        )
        self.browser.get(self.live_server_url + reverse('gp_report', args=[1, 1]))
        redirect_url = self.live_server_url + reverse('gpdetail_loc')
        self.browser.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    