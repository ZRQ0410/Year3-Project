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

    def test_user_sees_card_list(self):
        self.browser.get(self.live_server_url)
        element = self.browser.find_element(By.CLASS_NAME, 'cards')
        self.assertEquals(
            element.find_elements(By.CLASS_NAME, 'data-label')[0].text,
            "Total Evaluated GPs' Websites"
        )
        self.assertEquals(
            element.find_elements(By.CLASS_NAME, 'data-label')[1].text,
            "Total Evaluated Districts"
        )
        self.assertEquals(
            element.find_elements(By.CLASS_NAME, 'data-label')[2].text,
            "Evaluation Tool"
        )
        self.assertEquals(
            element.find_elements(By.CLASS_NAME, 'data-label')[3].text,
            "Guidelines"
        )
    
    def test_user_sees_pie_chart(self):
        self.browser.get(self.live_server_url)
        element = self.browser.find_element(By.ID, 'categories').get_attribute("innerHTML")
        assert("<canvas" in element)

    def test_user_sees_bar_chart(self):
        self.browser.get(self.live_server_url)
        element = self.browser.find_element(By.ID, 'top-err').get_attribute("innerHTML")
        assert("<canvas" in element)

    def test_user_sees_err_list(self):
        self.browser.get(self.live_server_url)
        alert = self.browser.find_element(By.ID, 'table-title')
        self.assertEquals(alert.text, "Level A")
    
    def test_analysis_button_redirects_to_home_page(self):
        self.browser.get(self.live_server_url)
        redirect_url = self.live_server_url + reverse('home')
        self.browser.find_element(By.CLASS_NAME, 'side-bar').find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_overall_button_redirects_to_home_page(self):
        self.browser.get(self.live_server_url)
        redirect_url = self.live_server_url + reverse('home')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[0].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_district_button_redirects_to_district_page(self):
        self.browser.get(self.live_server_url)
        redirect_url = self.live_server_url + reverse('districts')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[1].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_trend_button_redirects_to_trend_page(self):
        self.browser.get(self.live_server_url)
        redirect_url = self.live_server_url + reverse('trend')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[2].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    
    def test_gpdetail_button_redirects_to_gp_page(self):
        self.browser.get(self.live_server_url)
        redirect_url = self.live_server_url + reverse('gpdetail_loc')
        self.browser.find_elements(By.CLASS_NAME, 'nav-link')[3].click()
        self.assertEquals(
            self.browser.current_url,
            redirect_url
        )
    