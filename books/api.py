import requests
import json
from icecream import ic
import config
import urllib.request
from urllib.parse import urlencode, quote_plus, unquote
import pandas as pd
from pandas.io.json import json_normalize

SUBSCRIPTION_KEY = config.data_book_api_key
url = f'http://data4library.kr/api/loanItemSrch?authKey={config.data_book_api_key}&startDt=2022-07-10&endDt=2022-07-12&format=json'
response = urllib.request.urlopen(url).read()
json_object = json.loads(response)
body = json_object['response']
json_object = body['docs']
book_list = []
for i in range(50):
    book_list.append(json_object[i]['doc'])
print(book_list)

book_title = {book_list[i]['bookname'] for i in range(50)}
category = {book_list[i]['class_nm'] for i in range(50)}
isbn = {book_list[i]['isbn13'] for i in range(50)}
author = {book_list[i]['authors'] for i in range(50)}
book_img = {book_list[i]['bookImageURL'] for i in range(50)}

columns = ['isbn', 'author', 'book_title', 'category', 'book_img']


# file = open('book.json', "w+")
# file.write(json.dumps(json_object))
# print(type(json_object))
# print(json_object[0].keys)

# dataframe = json_normalize(json_object)
# print(dataframe)
