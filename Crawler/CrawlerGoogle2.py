#encoding=utf-8
import urllib2
import requests
import lxml.etree as etree
import simplejson as json
import os
import random
import time
import sys
def scrape_google_res(keyword):
    # url = 'https://www.google.com.au/search?output=search&sclient=psy-ab&q=%s'%(keyword)
    url = "https://www.google.com.hk/search?safe=strict&hl=zh-cn&site=&source=hp&q=%s&num=50"%(keyword)
    result = []
    #result = {'serp': [], 'adv': []}
    # 必须提供头信息，否则谷歌不响应。
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0',
        'Host': 'www.google.com.au'
    }
    req = urllib2.Request(url, headers=hdr)
    text = urllib2.urlopen(req).read()
    html = etree.HTML(text)
    serp_links = html.xpath("//h3[@class='r']/a")
    for serp_link in serp_links:
        result.append(serp_link.attrib['href'])
    # adv_links = html.xpath("//li[@class='ads-ad']/h3/a[last()]")
    # for adv_link in adv_links:
    #     result['adv'].append(adv_link.attrib['href'])
    return result

def getHtmlContent(url):
    # hea = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    ]
    # 在User-Agent列表里随机选择一个User-Agent
    user_agent = random.choice(ua_list)
    hea = {}
    hea['User-Agent'] = user_agent
    html = requests.get(url, headers=hea, timeout=20)
    html.encoding = 'utf-8'
    return html.text


def getJsonContent(fileName,title):
    in_srt = open(fileName, 'r').read()
    s = json.loads(in_srt)
    dir = {}
    for id in s:
        topid = id["topid"]
        dir[topid] = id[title]
    return dir
def getKeywordFormat(content):
    list = content.split(" ")
    keyWord = ""
    for i in range(len(list)):
        if i == len(list) - 1:
            keyWord +=  (list[i])
        else:
            keyWord += "%s+"%(list[i])
    return keyWord

def createFolder(path,name):
    isExists = os.path.exists(path+name)
    if not isExists:
        os.makedirs(path+name)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    #dir = getJsonContent("C:\\Users\\Administrator\\Desktop\\123\\2015_all_topics.json","title")
    dir={"MB442":"Bay+Bridge+accident"}
    filePath = "C:\\Users\\Administrator\\Desktop\\123\\2015_all_topics\\"
    for key in dir.keys():
        createFolder(filePath,key)
        value = dir.get(key)
        keyWord = getKeywordFormat(value)
        try:
            URLlist = scrape_google_res(str(keyWord))
            for i in range(len(URLlist)):
                try:
                    html = getHtmlContent(URLlist[i])
                    file = open(filePath+key+"\\"+key+"_"+str(i)+".txt",'w')
                    file.write(html)
                    file.close()
                except Exception as e:
                    print e
        except Exception as eURLlist:
            print key + ":" + keyWord
    #  print scrape_google_res("grilling+burgers")
    # print getHtmlContent("https://www.fitnessfirst.com.au/find-a-class/super-seniors/")


