
import urllib.request
from bs4 import BeautifulSoup

url = 'https://www.google.com.hk/search?q=hello&btnG=Search&safe=active&gbv=1'
ua_headers = {"user-Agent":"/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/58.0.3029.96 Safari/537.36"}
request = urllib.request.Request(url,headers= ua_headers)
response = urllib.request.urlopen(request)
html = response.read()  # 搜索结果页的内容
soup = BeautifulSoup(html,"html.parser")
print(soup.body.text.encode('utf-8','ignore').decode('utf-8'))

