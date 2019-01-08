#! /usr/bin/env python
# coding=utf-8
from sgmllib import SGMLParser
from urllib import urlopen
import urllib
import urllib2
import time
import re
import os, sys
import httplib
from urllib2 import Request, urlopen, URLError, HTTPError

httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

class GetIdList3(SGMLParser):
    def reset(self):
        self.IDlist = []
        self.flag = False
        self.getdata = False
        self.verbatim = 0
        SGMLParser.reset(self)

    def start_div(self, attrs):
        if self.flag == True:
            self.verbatim += 1
            return
        for k, v in attrs:
            if k == 'class' and v == 'c-abstract':
                self.flag = True
                self.getdata = True
                return

    def end_div(self):
        if self.verbatim == 0:
            self.flag = False
            self.getdata = False
        if self.flag == True:
            self.verbatim -= 1

    def handle_data(self, text):
        if self.getdata:
            self.IDlist.append(text)

def downloadpage(url, longid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    req = urllib2.Request(
        url=url,

        headers=headers
    )
    time1 = time.time()
    time2 = time1
    flag1 = 0
    while time2 - time1 < 5:
        try:

            raw = urllib2.urlopen(req, data=None, timeout=10).read()
        except IOError:
            pass
        except:
            time.sleep(1)
            raw2 = ""
            break
        else:
            flag1 = 1

            break
        time2 = time.time()
    if flag1 == 0:
        print("读取网页失败")
        #         writelog("读取网页失败-"+url+"-"+time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))+"\n")
        return
    global htmldir
    f = open(htmldir + longid + ".html", 'w')
    f.write(raw)
    f.close()
    print(longid)

def writelog(a):
    global logdir
    f = open(logdir, 'a')
    f.write(a)
    f.close()

def createdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

resultdir = r"d:\baidu"
rootdir = r"d:\baidu\source"
htmldir = resultdir + "\\" + "all_html" + "\\"
createdir(resultdir)
createdir(htmldir)

def writeurllist(unablelistdir, doc):
    unablelistdir = unablelistdir + "\\" + doc + ".txt"
    if not os.path.exists(unablelistdir):
        d = open(unablelistdir, 'w')
        d.close()
    d = open(unablelistdir, 'r')
    line = d.readline()
    h = {}
    while line:
        line = line.strip("\n")
        h[line] = 1
        line = d.readline()
    d.close()
    return h

time11 = 0
for file in os.listdir(rootdir):
    docid = file[:file.find(".")]
    docname = file[file.find("_") + 1:file.find(".txt")]
    f = open(rootdir + "\\" + file, 'r')
    a = f.read()
    a = a.replace("\xef\xbb\xbf", "")
    f.close()
    flag = 0
    j1index = 0
    while True:
        if j1index == len(a.split("\n")):
            break
        j1 = a.split("\n")[j1index]
        if len(j1) < 1:
            if j1index == 0:
                j1index += 1
                continue
            break
        j1 = j1.replace(" ", "+")
        j1 = j1.replace("\t", "+")
        #         print "j1before "+j1
        queryid = j1[:j1.find("_")]
        j1 = j1[j1.find("_") + 1:]
        j1 = j1.strip("+")
        #         print "j1 "+j1
        kd = j1

        url = "http://www.baidu.com/s?wd={0}&pn=0&rn=30&cl=3&gpc=stf%3D1486106703%2C1488525903%7Cstftype%3D1&tfflag=1".format(
            kd)

        print(url)
        time1 = time.time()
        time2 = time1
        flag1 = 0
        while time2 - time1 < 10:
            try:
                raw2 = urllib2.urlopen(url, data=None, timeout=1).read()
            except IOError:
                pass
            else:
                flag1 = 1
                break
            time2 = time.time()
        if flag1 == 0:
            continue
        if "<!--STATUS OK-->" not in raw2:
            if flag == 0:

                flag = 1
                time.sleep(10)
                continue
            else:
                flag = 0
                #                 writelog("读取搜索结果失败-{0}".format(kd)+"-"+time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))+"\n")
                j1index += 1
                continue
        if flag == 1:
            flag = 0
        resultnum = raw2.count(" class=\"result\" ") + raw2.count(
            "class=\"result-op c-container xpath-log\"") + raw2.count("class=\"result-op c-container\"") + raw2.count(
            "class=\"result c-container \"") + raw2.count("class=\"result c-container\"")
        if resultnum != 50:
            pass
        print(kd)
        for i1 in range(1, resultnum + 1):
            rankid = str(i1)
            longid = "{0}_{1}_{2}".format(docid, queryid, rankid)
            time11 = time.time()
            if i1 == resultnum:
                block = raw2[raw2.find("id=\"{0}\"".format(str(i1))):]
                block = block[block.find("id=\"{0}\"".format(str(i1))):block.find("</div></div>")]
            else:
                block = raw2[raw2.find("id=\"{0}\"".format(str(i1))):raw2.find("id=\"{0}\"".format(str(i1 + 1)))]
            raw2 = raw2[raw2.find("id=\"{0}\"".format(str(i1))):]
            lister3 = GetIdList3()
            lister3.feed(block)
            n3 = lister3.IDlist

            snippet2 = ""
            for i3 in n3:
                snippet2 = snippet2 + i3
            block2 = block[block.find("<h3"):block.find("</h3>") + 5]
            link = ""
            if "<a href=\"" in block2:
                link = block2[block2.find("<a href=\"") + 9:block2.find("\" target=")]
            elif "href = \"" in block2:
                link = block2[block2.find("href = \"") + 8:block2.find("target=")]
                link = link[:link.rfind("\"")]
            elif "\"_blank\" href=\"" in block2:
                link = block2[block2.find("\"_blank\" href=\"") + 15:block2.find("\" >")]
            try:
                req = Request(link)
                response = urlopen(req, data=None, timeout=10)

                link = response.geturl()
            except:
                pass
            downloadpage(link, longid)
        j1index += 1
