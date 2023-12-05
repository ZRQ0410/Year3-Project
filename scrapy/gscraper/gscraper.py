from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus
import time
import random
import pandas as pd
import csv


class Gscraper:
    def __init__(self, nhs_data: pd.DataFrame, filename: str):
        # input data frame: use gp, postcode columns
        self.nhs_data = nhs_data

        # output data frame: collect overview page url and store into 'nhs_url'
        self.links_df = pd.DataFrame(columns=['gp', 'postcode', 'nhs_url'])
        self.links_df[['gp', 'postcode']] = self.nhs_data[['gp', 'postcode']]
        self._setup_driver()

        # write while scraping, in case there are errors occurring during scraping
        self.file = open(filename, 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['gp', 'postcode', 'nhs_url'])

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
        """
        Preprocess the keyword: "postcode gp_name nhs gp overview" (put postcode first to make sure webpage contains the correct postcode). Then encode this into url form.
        Collect the results on the first page returned by Google search engine. Only collect the link with "www.nhs.uk/services/gp-surgery" to make sure it is the nhs overview page.
        """
        gp = row['gp']
        postcode = row['postcode']

        # remove '-' in the gp string for searching
        if '-' in gp:
            gp = gp.replace('-', '')

        # encode keywords into url, replace spaces with "+"
        keyword = f"{postcode} {gp} nhs gp overview"
        self.driver.get("https://www.google.com/search?q=" +
                        quote_plus(keyword))
        time.sleep(random.uniform(1.7, 2.2))

        # get the links on the first page that the chrome returned
        results = self.driver.find_element(
            By.ID, "search").find_elements(By.TAG_NAME, 'a')

        for i in range(len(results)):
            link = results[i].get_attribute('href')
            # if the result does not contain 'href' (Eg. google returns a map), skip and get next
            if link is None:
                continue
            # only collect the link which contains 'services/gp-surgery', make sure to get nhs overview related page
            if 'www.nhs.uk/services/gp-surgery' in link:
                print(f"{row['gp']},{postcode},{link}")
                # save to file during scraping
                self.writer.writerow([row['gp'], postcode, link])
                return link
        else:
            self.writer.writerow([row['gp'], postcode, None])
            return None

    def scrape_nhs_link(self):
        try:
            self.links_df['nhs_url'] = self.links_df.apply(
                lambda x: self._scrape_link(x), axis=1)

        except Exception as e:
            print('Error', e)
            self.file.close()

    def write2csv(self, docname):
        """
        Write all the results of the scraper into a csv file, after finish scraping.
        """
        self.links_df.to_csv(docname, index=False)
