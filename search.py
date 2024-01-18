


import requests
import sys
url = sys.argv[1]

res = requests.get(url)
from bs4 import BeautifulSoup

soup = BeautifulSoup(res.text, 'html.parser')
trs = soup.find_all('tr')
log_links = []
FAIL_STATUSES = ['dead', 'fail']
for tr in trs:
    tds = tr.find_all('td', attrs={"data-title": "Status"})
    do_append = False
    for td in tds:
        for status in FAIL_STATUSES:
            if status in td.text:
                do_append = True
    if do_append:
        tds = tr.find_all('td', attrs={"data-title": "Links"})
        for td in tds:
            log_links.append(td.find('a').get('href'))


print('Found {len(log_links)} failing runs')
print('------------------------------------------')

keywords = ['Segmentation fault', 'ceph_assert', 'Caught signal (Aborted)', 'Traceback']
for link in log_links:
    print('------------------------------------------')
    print(f'Getting info from {link}')
    print('------------------------------------------')
    response = requests.get(link, timeout=5)
    lines = response.text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        for keyword in keywords:
            if keyword in line:
                # print next 20 lines
                for j in range(i, i+20):
                    if j < len(lines):
                        print(lines[j])
                    else:
                        break
                break
        i += 1

