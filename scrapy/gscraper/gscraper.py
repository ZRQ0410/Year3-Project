from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException
from urllib.parse import quote_plus
import time
import random
import pandas as pd


class Gscraper:
    def __init__(self, nhs_data: pd.DataFrame):
        # input data frame: use gp, postcode columns
        self.nhs_data = nhs_data
        # output data frame: collect overview page url and store into 'nhs_url'
        self.links_df = pd.DataFrame(columns=['gp', 'postcode', 'nhs_url'])
        self.links_df[['gp', 'postcode']] = self.nhs_data[['gp', 'postcode']]
        self._setup_driver()

    def _setup_driver(self):
        # avoid detection
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--lang=en-GB")
        # silent mode
        # options.add_argument('--headless')
        # update chrome automatically
        version = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(version, options=options)

    def close_driver(self):
        self.driver.close()

    def _scrape_link(self, row):
        gp = row['gp']
        postcode = row['postcode']

        # remove '-' in the string
        if '-' in gp:
            gp = gp.replace('-', '')

        # encode keywords into url, replace spaces with "+"
        keyword = f"{gp} {postcode} nhs gp overview"
        self.driver.get("https://www.google.com/search?q=" +
                        quote_plus(keyword))
        time.sleep(random.uniform(1.8, 2.2))

        # get the first 10 links that the chrome returned
        results = self.driver.find_element(
            By.ID, "search").find_elements(By.TAG_NAME, 'a')
        for i in range(10):
            link = results[i].get_attribute('href')
            # only collect the link which contains 'services/gp-surgery', make sure to get nhs overview related page
            if 'www.nhs.uk/services/gp-surgery' in link:
                print(link)
                return link
        else:
            return None

        # except NoSuchElementException:
        #     WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@title='reCAPTCHA']")))
        #     time.sleep(random.uniform(2, 2.5))
        #     cap = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='recaptcha-checkbox-border']"))).click()
        #     driver.switch_to.default_content()
        #     time.sleep(random.uniform(1, 1.5))

    def scrape_nhs_link(self):
        self.links_df['nhs_url'] = self.links_df.apply(
            lambda x: self._scrape_link(x), axis=1)

    def write2csv(self, docname):
        self.links_df.to_csv(docname, index=False)
