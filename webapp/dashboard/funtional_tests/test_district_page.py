from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

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

    def test_user_sees_err_map(self):
        self.browser.get(self.live_server_url + reverse('districts'))
        label = self.browser.find_element(By.CLASS_NAME, 'btnA1')
        self.assertEquals(
            label.text,
            "Error"
        )
        err_map = self.browser.find_element(By.ID, 'mean-err').get_attribute("innerHTML")
        self.assertIn('<canvas', err_map)
    
    def test_user_sees_likely_err_map(self):
        self.browser.get(self.live_server_url + reverse('districts'))
        label = self.browser.find_element(By.CLASS_NAME, 'btnA2')
        self.assertEquals(
            label.text,
            "Likely Error"
        )
        err_map = self.browser.find_element(By.ID, 'mean-likely').get_attribute("innerHTML")
        self.assertIn('<canvas', err_map)
    
    def test_user_sees_potential_err_map(self):
        self.browser.get(self.live_server_url + reverse('districts'))
        label = self.browser.find_element(By.CLASS_NAME, 'btnA3')
        self.assertEquals(
            label.text,
            "Potential Error"
        )
        err_map = self.browser.find_element(By.ID, 'mean-potential').get_attribute("innerHTML")
        self.assertIn('<canvas', err_map)
    
    def test_user_sees_Alevel_map(self):
        self.browser.get(self.live_server_url + reverse('districts'))
        label = self.browser.find_element(By.CLASS_NAME, 'btnB1')
        self.assertEquals(
            label.text,
            "A"
        )
        level_map = self.browser.find_element(By.ID, 'A-percent').get_attribute("innerHTML")
        self.assertIn('<canvas', level_map)
    
    def test_user_sees_AAlevel_map(self):
        self.browser.get(self.live_server_url + reverse('districts'))
        label = self.browser.find_element(By.CLASS_NAME, 'btnB2')
        self.assertEquals(
            label.text,
            "AA"
        )
        level_map = self.browser.find_element(By.ID, 'AA-percent').get_attribute("innerHTML")
        self.assertIn('<canvas', level_map)
    
    def test_user_sees_AAAlevel_map(self):
        self.browser.get(self.live_server_url + reverse('districts'))
        label = self.browser.find_element(By.CLASS_NAME, 'btnB3')
        self.assertEquals(
            label.text,
            "AAA"
        )
        level_map = self.browser.find_element(By.ID, 'AAA-percent').get_attribute("innerHTML")
        self.assertIn('<canvas', level_map)
    
    def test_analysis_button_redirects_to_home_page(self):
        self.browser.get(self.live_server_url + reverse('districts'))
        redirect_url = self.live_server_url + reverse('home')
        self.browser.find_element(By.CLASS_NAME, 'side-bar').find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_overall_button_redirects_to_home_page(self):
        self.browser.get(self.live_server_url + reverse('districts'))
        redirect_url = self.live_server_url + reverse('home')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[0].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_district_button_redirects_to_district_page(self):
        self.browser.get(self.live_server_url + reverse('districts'))
        redirect_url = self.live_server_url + reverse('districts')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[1].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_trend_button_redirects_to_trend_page(self):
        self.browser.get(self.live_server_url + reverse('districts'))
        redirect_url = self.live_server_url + reverse('trend')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[2].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_gpdetail_button_redirects_to_gp_page(self):
        self.browser.get(self.live_server_url + reverse('districts'))
        redirect_url = self.live_server_url + reverse('gpdetail_loc')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[3].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    