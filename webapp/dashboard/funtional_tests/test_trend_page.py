from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

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

    def test_user_sees_line_plot(self):
        self.browser.get(self.live_server_url + reverse('trend'))
        plot = self.browser.find_element(By.ID, 'trend-cat').get_attribute("innerHTML")
        self.assertIn('<canvas', plot)
    
    def test_user_sees_bar_plot(self):
        self.browser.get(self.live_server_url + reverse('trend'))
        plot = self.browser.find_element(By.ID, 'trend-err').get_attribute("innerHTML")
        self.assertIn('<canvas', plot)
    
    def test_analysis_button_redirects_to_home_page(self):
        self.browser.get(self.live_server_url + reverse('trend'))
        redirect_url = self.live_server_url + reverse('home')
        self.browser.find_element(By.CLASS_NAME, 'side-bar').find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_overall_button_redirects_to_home_page(self):
        self.browser.get(self.live_server_url + reverse('trend'))
        redirect_url = self.live_server_url + reverse('home')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[0].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_district_button_redirects_to_districts_page(self):
        self.browser.get(self.live_server_url + reverse('trend'))
        redirect_url = self.live_server_url + reverse('districts')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[1].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_trend_button_redirects_to_trend_page(self):
        self.browser.get(self.live_server_url + reverse('trend'))
        redirect_url = self.live_server_url + reverse('trend')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[2].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_gpdetail_button_redirects_to_gp_page(self):
        self.browser.get(self.live_server_url + reverse('trend'))
        redirect_url = self.live_server_url + reverse('gpdetail_loc')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[3].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )