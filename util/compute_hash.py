__author__ = 'raistlin'

from urllib.request import urlopen
from urllib.request import Request
import urllib
anon_nick = "anon-8d68c519ee4d9fc"
receipt = "https://api.connected2.me/b/receipt_android"

data = "nick=bigblackhole&password=3215987a&token=1&product_id=plus30"

data = urllib.parse.urlencode({"nick":"bigblackhole", "password":"3215987a", "token": "1", "product_id":"plus30"})

binary_data = data.encode('utf8')
print ("sa")

# make a string with the request type in it:
method = "POST"


hdr = {
           'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive',
           'Referer': 'https://connected2.me'}
request = Request(receipt, headers= hdr, data=binary_data)
# add any other information you want
# request.add_header("Content-Type",'application/json')
# overload the get method function with a small anonymous function...
request.get_method = lambda: method
# try it; don't forget to catch the result

connection = urlopen(request).read()
print(connection)