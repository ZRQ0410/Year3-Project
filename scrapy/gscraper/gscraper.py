from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException
import time
import random
import pandas as pd
import sys
import os


def init_df():
    data = pd.read_csv('scraper/nhsdata.csv')
    gp_df = pd.DataFrame(columns=['gp', 'nhs_url'])
    gp_df['gp'] = data['gp'].unique()
    return gp_df


def setup_driver():
    # avoid detection
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=en-GB")
    # silent mode
    # options.add_argument('--headless')

    # update chrome automatically
    version = ChromeDriverManager().install()

    driver = webdriver.Chrome(version, options=options)
    return driver


def close_driver():
    driver.close()


def scrape_nhs_link(gp):
    # deal with '&' in the name
    if '&' in gp:
        gp = gp.replace('&', '+26%+')

    driver.get("https://www.google.com/search?q=" + gp + "+nhs+gp+overview")
    time.sleep(random.uniform(1.7, 2))

    # get the first 10 links that the chrome returned
    results = driver.find_element(
        By.ID, "search").find_elements(By.TAG_NAME, 'a')
    for i in range(10):
        link = results[i].get_attribute('href')
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


def write2csv(docname):
    gp_df.to_csv(docname, index=False)


if __name__ == "__main__":
    # scrape nhs overview url
    gp_df = init_df()
    driver = setup_driver()
    gp_df['nhs_url'] = gp_df['gp'].apply(lambda gp: scrape_nhs_link(gp))
    close_driver()
    write2csv("nhslinks.csv")

    # clean data
    sys.path.append(
        "C:\\Users\\12927\\Desktop\\Year3 Project\\scrapy\\gscraper")
    # print(sys.path)
    from cleaner import Cleaner

    cwd = os.getcwd()
    if 'gscraper' in cwd:
        path = os.path.join(cwd, "nhslinks.csv")
    else:
        path = os.path.join(cwd, "gscraper/nhslinks.csv")
    df = pd.read_csv(path)

    # drop na
    df_not_null = Cleaner.clean_na(df)
    # remove review url, convert it to url of the overview page
    cleaned_df = Cleaner.correct_url(df_not_null)
    cleaned_df.to_csv("gscraper/cleaned_nhslinks.csv", index=False)
