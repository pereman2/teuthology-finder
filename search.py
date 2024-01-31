


import requests
import datetime
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
errors = {}
def without_prefix(s):
    split = s.split(' ')
    is_log_line = False
    try:
        datetime.datetime.fromisoformat(split[0])
        is_log_line = True
    except:
        pass
    if is_log_line:
        without_date = ' '.join(split[1:])
        split_machine = without_date.split(':')
        without_prefix = ' '.join(split_machine[2:])
        return without_prefix
    return s

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
                # print next 30 lines
                error = ""
                for j in range(i, i+30):
                    if j < len(lines):
                        print(lines[j])
                        error += without_prefix(lines[j]) + "\n" 
                    else:
                        break
                if error not in errors:
                    errors[error] = 1
                else:
                    errors[error] += 1
                break
        i += 1

import json
print(json.dumps(errors, indent=2))
for k, v in errors.items():
    print()
    print()
    print("Error count = ", v)
    print(k)
