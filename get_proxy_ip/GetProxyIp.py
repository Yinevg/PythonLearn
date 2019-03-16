import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://www.xicidaili.com/nn/{}'
checkUrl = 'http://httpbin.org/ip'
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
file_content = []
for i in range(1, 6):
    # 获取请求结果
    resp = requests.get(url=base_url.format(i), headers=headers)
    bsObj = BeautifulSoup(resp.text, 'html.parser')
    ipList = bsObj.find('table', {'id': 'ip_list'}).findAll('tr')
    # 去除表头
    for ip in ipList[1:]:
        tds = ip.select('td')
        proxy_ip = tds[1].get_text()
        proxy_port = tds[2].get_text()
        proxy = proxy_ip + ':' + proxy_port
        proxies = {
            'http': proxy,
            'https': proxy
        }
        try:
            print('check proxy %s' % proxy)
            checkResp = requests.get(url=checkUrl, proxies=proxies, timeout=1)
            # 检查是否为有效ip
            if proxy_ip in json.loads(checkResp.text)["origin"]:
                file_content.append(proxy)
                print('proxy %s is valid' % proxy)
            else:
                print('proxy %s is invalid' % proxy)
        except Exception as e:
            print('proxy %s is invalid : %s' % (proxy, e))
with open("proxies.txt", "w", encoding="utf-8") as f:
    for line in file_content:
        f.write(line + '\n')
print('total: %s' % len(file_content))
