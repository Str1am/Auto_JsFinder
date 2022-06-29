#!/usr/bin/env python
# coding: utf-8
# By Threezh1
# Modify By Str1am

import httpx, argparse, sys, re
from requests.packages import urllib3
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import threading,time


# Regular expression comes from https://github.com/GerbenJavado/LinkFinder
def extract_URL(JS):
    pattern_raw = r"""
	  (?:"|')                               # Start newline delimiter
	  (
	    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
	    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
	    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
	    |
	    ((?:/|\.\./|\./)                    # Start with /,../,./
	    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
	    [^"'><,;|()]{1,})                   # Rest of the characters can't be
	    |
	    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
	    [a-zA-Z0-9_\-/]{1,}                 # Resource name
	    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
	    (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
	    |
	    ([a-zA-Z0-9_\-]{1,}                 # filename
	    \.(?:php|asp|aspx|jsp|json|
	         action|html|js|txt|xml)             # . + extension
	    (?:\?[^"|']{0,}|))                  # ? mark with parameters
	  )
	  (?:"|')                               # End newline delimiter
	"""
    pattern = re.compile(pattern_raw, re.VERBOSE)
    result = re.finditer(pattern, str(JS))
    if result == None:
        return None
    js_url = []
    return [match.group().strip('"').strip("'") for match in result
            if match.group() not in js_url]


# Get the page source
def Extract_html(URL):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"}
    try:
        raw = httpx.get(URL, headers=header, timeout=3, verify=False)
        raw = raw.content.decode("utf-8", "ignore")
        return raw
    except:
        return None

def _request(req_url,path):
    try:
        req_get = httpx.get(req_url + path,verify=False)
        if req_get.status_code == 200 and req_get.headers['Content-Type'] != 'text/html; charset=utf-8' and req_get.headers['Content-Type'] != 'image/png' and req_get.headers['Content-Type'] != 'image/jpeg' and 'html' not in req_get.text:
            print("请求api路径：" + req_url + path + "\n" +  "响应包为：" + req_get.text)

        req_post = httpx.post(req_url + path,verify=False)
        if req_post.status_code == 200 and req_post.headers['Content-Type'] != 'text/html; charset=utf-8' and req_post.headers['Content-Type'] != 'image/png' and req_post.headers['Content-Type'] != 'image/jpeg' and 'html' not in req_post.text:
            print("请求api路径：" + req_url + path + "\n" + " 响应包为：" + req_post.text)
    except:
        pass

def get_body(js_url):
    # 处理当前的url，以js文件所在host发送request请求
    url_raw = urlparse(js_url)
    protocol = url_raw.scheme
    host = url_raw.netloc
    req_url = protocol + "://" + host

    #获取js
    link_url = giveresult(js_url)   #获取从js中得到的链接
    threads = []
    for path in link_url:
        t = threading.Thread(target=_request, args=(req_url,path))
        t.start()
        threads.append(t)

def get_new_body(js_url,custom_url):
    #获取js
    link_url = giveresult(js_url)   #获取从js中得到的链接
    threads = []
    print(custom_url)
    for path in link_url:
        t = threading.Thread(target=_request, args=(custom_url,path))
        t.start()
        threads.append(t)


def find_by_jsUrl(file_url):
    urls = []
    temp_urls = find_by_url(file_url)
    print(" Find " + str(len(temp_urls)) + " URL in " + file_url)
    for temp_url in temp_urls:
        if temp_url not in urls:
            urls.append(temp_url)
    return urls


def giveresult(js_url):
    links = []
    if js_url == None:
        return None
    js_content = Extract_html(js_url)
    url_link = extract_URL(js_content)

    #筛选一下url
    for each in url_link:
        if each.endswith('.js') or each.endswith('.png') or each.endswith('.ivo') or each.endswith('.jpg') or each.endswith('.vue') or each.endswith('svg') or each.endswith('.css') or each.startswith('http') or each.startswith('./') or  each.startswith('../'):
            pass
        else:
            links.append(each)
    return links


if __name__ == "__main__":
    js_url = input("Please enter the path of the js file: ")
    js_link = giveresult(js_url)
    print("————————正在获取api接口——————————")
    for link in js_link:
        print(link)
    print("————————正在对api发送请求——————————")
    get_body(js_url)
    print("————————输入自定义请求接口——————————")
    time.sleep(1)
    custom_url = input("Please enter api url: ")
    #print(js_url)
    get_new_body(js_url,custom_url)
