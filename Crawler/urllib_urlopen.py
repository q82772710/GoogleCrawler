#encoding = utf-8
import urllib.request

ua_headers = {"user-Agent":"/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"}

request = urllib.request.Request("https://www.google.com.au/search?output=search&sclient=psy-ab&q=I+am+a+student",headers= ua_headers)

response = urllib.request.urlopen(request)

html = response.readlines()



# file = open("C:\\Users\\Administrator\\Desktop\\123.txt",'w',encoding="utf-8")

# file.write(str(html))

# file.close()
print(html)