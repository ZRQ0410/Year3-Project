"""
Divide all issue IDs into three sets:   
    1) issues in level A
    2) issues in level AA
    3) issues in level AAA
Each issue ID is only mapped to one set.
"""

import requests
from bs4 import BeautifulSoup

total_ids = []
for i in range(7, 10):
    url = 'https://websiteaccessibilitychecker.com/guideline/view_guideline.php?id=' + str(i)
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html')
    tables = soup.find_all('tbody')
    issue_ids = set()
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            issue_id = row.find_all('td')[-1].text
            issue_ids.add(issue_id)

    total_ids.append(issue_ids)

id_A = total_ids[0]
id_AA = total_ids[1] - total_ids[0]
id_AAA = total_ids[2] - total_ids[1]

# print(id_A)
# print(id_AA)
# print(id_AAA)

# write to local file:
# line 1: level A id
# line 2: level AA id
# line 3: level AAA id
with open('check_ids.txt', 'w') as f:
    f.write(','.join(id_A) + '\n')
    f.write(','.join(id_AA) + '\n')
    f.write(','.join(id_AAA) + '\n')

# read the three sets from files
# with open('issue_ids.txt', 'r') as f:
#     print(set(map(int, f.readlines()[0].split(','))))