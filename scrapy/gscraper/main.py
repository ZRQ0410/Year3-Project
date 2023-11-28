from Gscraper import Gscraper
from Cleaner import Cleaner
import pandas as pd


def scrape():
    nhs_data = pd.read_csv('../data/nhsdata.csv', usecols=['gp', 'postcode'])
    scraper = Gscraper(nhs_data)
    scraper.scrape_nhs_link()
    scraper.close_driver()
    # write to csv file
    scraper.write2csv('../data/nhslinks.csv')
    return scraper.links_df


def clean(links_df):
    cleaner = Cleaner()
    # drop None value
    links_notnull = cleaner.clean_na(links_df)
    # convert url to the correct form
    cleaned_links = cleaner.correct_url(links_notnull)
    cleaned_links.to_csv("../data/nhslinks_cleaned.csv", index=False)


if __name__ == '__main__':
    # scrape the nhs overview link
    links_df = scrape()

    # clean and store the data
    clean(links_df)
