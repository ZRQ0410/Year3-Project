from Gscraper import Gscraper
from Cleaner import Cleaner
import pandas as pd


def scrape():
    nhs_data = pd.read_csv('../data/gp_table.csv', usecols=['gp', 'postcode'])
    # save to nhslinks.csv while scraping
    scraper = Gscraper(nhs_data, '../data/nhslinks.csv')
    scraper.scrape_nhs_link()
    scraper.close_driver()
    # write to csv file AFTER finishing scraping
    # scraper.write2csv('test.csv')
    return scraper.links_df


def clean(links_df):
    cleaner = Cleaner()
    # convert url to the correct form
    cleaned_links = cleaner.correct_url(links_df)
    cleaned_links.to_csv("../data/nhslinks_cleaned.csv", index=False)


if __name__ == '__main__':
    # scrape the nhs overview link
    links_df = scrape()

    # clean and store the data
    links_df = pd.read_csv('../data/nhslinks.csv')
    clean(links_df)
