# encoding: utf-8
import requests
import string
import json
import re
from google.cloud import translate
from oauth2client.client import GoogleCredentials


from bs4 import BeautifulSoup


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.text
    except:
        print("Get HTML Text Failed!")
        return 0


def google_translate_EtoC(to_translate, from_language="en", to_language="ch-CN"):
    # 根据参数生产提交的网址
    base_url = "https://translate.google.cn/m?hl={}&sl={}&ie=UTF-8&q={}".encode()
    url = base_url.format(to_language, from_language, to_translate)

    # 获取网页
    html = getHTMLText(url)
    if html:
        soup = BeautifulSoup(html, "html.parser")

    # 解析网页得到翻译结果
    try:
        result = soup.find_all("div", {"class": "t0"})[0].text
    except:
        print("Translation Failed!")
        result = ""

    return result


def google_translate_CtoE(to_translate, from_language, to_language="en"):
    # 根据参数生产提交的网址

    base_url = "https://translate.google.cn/m?hl={}&sl={}&ie=UTF-8&q={}"
    url = base_url.format(to_language, from_language, to_translate)

    #print(url)

    # 获取网页
    html = getHTMLText(url)

    if html:
        soup = BeautifulSoup(html, "html.parser")

    # 解析网页得到翻译结果
    try:
        result = soup.find_all("div", {"class": "t0"})[0].text
    except:
        print("Translation Failed!")
        result = ""

    return result

def getStrandString(l):
    try:
        line = str(l).translate(string.maketrans("", ""), string.punctuation)
        list = line.split(" ")
        s = ""
        for l in list:
            if l.isalpha() == False and l.strip() != "":
                s += l +" "
        return s
    except:
        return ""

def translate1(readFilePath,writeFilePath):
    readFile = open(readFilePath,'r',encoding="utf-8")
    lines = readFile.readlines()
    writeFile = open(writeFilePath,'w',encoding="utf-8")
    for line in lines:
        dic = json.loads(line.strip())
        id = dic['id']
        text = dic['text'].replace('\n',' ').replace('\r',' ')
        lang = dic['lang']
        #strandString = getStrandString(text)
        # if strandString.strip() != "":
        #     result = google_translate_CtoE(strandString,"suto")
        if lang == "en":
            #result = google_translate_CtoE(text.encode("utf-8"), "suto")
            list = str(text).split(" ")
            s =""
            for l in list:
                if l.strip() != "":
                    s += l + " "
            writeFile.write(str(id) + "\t" +s+"\n")
        # else:
        #     writeFile.write(str(id) + "\t" + str(text.encode('utf-8'))+"\n")
    readFile.close()
    writeFile.close()


def translate2(readFilePath,writeFilePath):
    readFile = open(readFilePath,'r',encoding="utf-8")
    lines = readFile.readlines()
    writeFile = open(writeFilePath,'w',encoding="utf-8")
    for line in lines:
        list = line.strip().split("\t")
        list[1]

    readFile.close()
    writeFile.close()







def main():
    #words = " पर भी joke बना रहे है भड़वे #RIP इंसानियत"
    #words = "ktm:9843552882 biratnagar:9862005225 chitawan:9855065135 jhapa:9817976211 butwal:9812900905 रगत चाहिएको खन्डमा सम्पर्क गरौ #Nepal"
    #print(google_translate_CtoE(words,'auto'))
    paraPath ="C:\\Users\\Administrator\\Desktop\\Fire2017\\Fire2017-IRMiDis-data\\microblogs-crawl-directory\\"
    translate(paraPath+"allData.txt",paraPath+"translate1.txt")



if __name__ == "__main__":
    #main()
    #
    # l = "RT % ^ 33@bhakt11: @narendramodi जी और उनके मंत्री तो ,#earthquake  देश नही विदेश में भी भारतीय को मदद कर रहे   #WhatNextAK?   https://t.co/HuNZsx…"
    # l="RT @CNNMoney: A major earthquake was the last thing Nepal needed. Initial damage estimate: $5B http://t.co/gBOZ1GcVOi"
    # line = l.translate(string.maketrans("", ""), string.punctuation)
    # list = line.split(" ")
    # for l in list:
    #     if l.isalpha() == False and l.strip() != "":
    #         print(l)

    result = service.activities().list(userId='me', collection='public').execute()
    tasks = result.get('items', [])
    for task in tasks:
        print
        task['title']

    credentials = GoogleCredentials.get_application_default()

    # Instantiates a client
    translate_client = translate.Client()

    # The text to translate
    text = u'Hello, world!'
    # The target language
    target = 'ru'

    # Translates some text into Russian
    translation = translate_client.translate(
        text,
        target_language=target)

    print(u'Text: {}'.format(text))
    print(u'Translation: {}'.format(translation['translatedText']))