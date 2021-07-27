import re
import requests as rq
import json


data = rq.get(
    "https://www.cwb.gov.tw/Data/js/info/Info_Town.js?v=20200817")


# for item in data:
#     input(item)
result = re.search(r'({.*)', data.text, re.S).group(0).rstrip(';')
result.replace('''true''', ''':true"''')

# for item in result:
#     input(item)
print(eval(result))