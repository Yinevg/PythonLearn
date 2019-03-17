import json
import random

import requests
from bs4 import BeautifulSoup

base_url = 'https://www.xicidaili.com/nn/{}'
checkUrl = 'http://httpbin.org/ip'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
file_content = []
for i in range(1, 6):
    proxies = {}
    # 从已获取的代理IP中随机取一个来获取代理列表
    if len(file_content) > 0:
        random_proxy = random.sample(file_content, 1)[0]
        proxies['http'] = random_proxy
        proxies['https'] = random_proxy
    # 获取请求结果
    try:
        resp = requests.get(url=base_url.format(i), headers=headers, proxies=proxies)
    except Exception as e:
        # 使用代理请求失败，移除该代理
        if len(file_content) > 0:
            file_content.remove(proxies['http'])
            print('remove proxy %s: %s' % (proxies['http'], e))
        continue
    # 判断请求是否成功
    if resp.status_code != requests.codes.ok:
        print("get proxy list fail : %s" % resp.status_code)
        continue
    # 页面解析
    bsObj = BeautifulSoup(resp.text, 'html.parser')
    ipList = bsObj.find('table', {'id': 'ip_list'}).findAll('tr')
    # 去除表头
    for ip in ipList[1:]:
        tds = ip.select('td')
        proxy_ip = tds[1].get_text()
        proxy_port = tds[2].get_text()
        proxy = proxy_ip + ':' + proxy_port
        check_proxies = {
            'http': proxy,
            'https': proxy
        }
        try:
            print('check proxy %s' % proxy)
            checkResp = requests.get(url=checkUrl, headers=headers, proxies=check_proxies, timeout=1)
            # 检查是否为有效ip
            if proxy_ip in json.loads(checkResp.text)["origin"]:
                file_content.append(proxy)
                print('proxy %s is valid' % proxy)
            else:
                print('proxy %s is invalid' % proxy)
        except Exception as e:
            print('proxy %s is invalid : %s' % (proxy, e))
if len(file_content) > 0:
    with open("proxies.txt", "w", encoding="utf-8") as f:
        for line in file_content:
            f.write(line + '\n')
print('total: %s' % len(file_content))
