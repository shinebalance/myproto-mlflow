import sys
import requests

import config


# setURL
URL = config.TARGET_URL

r = requests.get(URL)

encoding = r.headers['Content-Encoding']
print(f'Encoding:{encoding}')

r.encoding = encoding

print(r.text)
