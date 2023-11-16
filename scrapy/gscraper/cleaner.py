import pandas as pd


class Cleaner:
    def __init__(self):
        pass

    @staticmethod
    def clean_na(df):
        return df.dropna()

    @staticmethod
    def correct_url(df):
        new = df.copy()
        new['nhs_url'] = df['nhs_url'].apply(
            lambda url: Cleaner.__remove_review(url))
        return new

    def __remove_review(url):
        # remove the review part, convert it to the url of the overview page
        s1 = "/leave-a-review"
        s2 = "/ratings-and-reviews"
        if s1 in url or s2 in url:
            if s1 in url:
                index = url.find(s1)
            elif s2 in url:
                index = url.find(s2)
            return url[:index]
        return url
