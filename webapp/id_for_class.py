"""
Get issue ids for each classification (Perceivable, Operable, Understandable, Robust) for three levels A, AA, AAA.
"""
import requests, json
from bs4 import BeautifulSoup

def get_issue_ids(level):
    if level == 'A':
        res = requests.get('https://websiteaccessibilitychecker.com/guideline/view_guideline.php?id=7')
    elif level == 'AA':
        res = requests.get('https://websiteaccessibilitychecker.com/guideline/view_guideline.php?id=8')
    else:
        res = requests.get('https://websiteaccessibilitychecker.com/guideline/view_guideline.php?id=9')
    soup = BeautifulSoup(res.text, 'html')
    tables = soup.find_all('tbody')
    issue_ids = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            issue_id = row.find_all('td')[-1].text
            issue_ids.append(issue_id)
    return issue_ids

# for sc in guidline A level
issue_ids = get_issue_ids('A')
idx1 = issue_ids.index('86')
class1 = issue_ids[:idx1+1]
idx2 = issue_ids.index('174')
class2 = issue_ids[idx1+1:idx2+1]
class3 = issue_ids[idx2+1:-1]
class4 = {issue_ids[-1]}

# for sc in guidline AA level
issue_ids = get_issue_ids('AA')
idx1 = issue_ids.index('11')
class1.extend(issue_ids[:idx1+1])
idx2 = issue_ids.index('47')
class2.extend(issue_ids[idx1+1:idx2+1])
class3.extend(issue_ids[idx2+1:-1])

# for sc in guidline AAA level
issue_ids = get_issue_ids('AAA')
idx1 = issue_ids.index('253')
class1.extend(issue_ids[:idx1+1])
idx2 = issue_ids.index('266')
class2.extend(issue_ids[idx1+1:idx2+1])
class3.extend(issue_ids[idx2+1:-1])

# remove duplicate id
class1 = set(class1)
class2 = set(class2)
class3 = set(class3)

classes = {1: list(class1), 2: list(class2), 3: list(class3), 4: list(class4)}

# write to json file
with open('dashboard/data/classes.json', 'w') as f:
        json.dump(classes, f)