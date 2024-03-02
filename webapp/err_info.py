import requests, json
from bs4 import BeautifulSoup

# get all Check IDs for all three levels: A, AA, AAA
all_ids = []
for i in range(7, 10):
    res = requests.get("https://websiteaccessibilitychecker.com/guideline/view_guideline.php?id="+str(i))
    soup = BeautifulSoup(res.text, 'html')
    data = soup.find(class_='output-form').find_all(class_='data')
    for d in data:
        row = d.find('tbody').find_all('tr')
        for r in row:
            all_ids.append(r.find_all('td')[-1].text)

all_ids = set(all_ids)
print(all_ids)

err_info = {}
# for each id get its: sc, error message, requirement description
for id in all_ids:
    res = requests.get("https://websiteaccessibilitychecker.com/checker/suggestion.php?id=" + id)
    soup = BeautifulSoup(res.text, 'html')
    sc = soup.find(class_='output-form').find_all('li')[-1].find(class_='padding_left').text
    msg = soup.find(class_='output-form').find_all(class_='msg')[4].text
    descr = soup.find(class_='output-form').find_all(class_='msg')[3].text
    err_info[id] = {'sc': sc, 'msg': msg, 'descr': descr}

# save to json
with open('dashboard/data/err_info.json', 'w') as f:
        json.dump(err_info, f)
