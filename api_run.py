

import requests
endpoint = 'http://127.0.0.1:8000/api/product/delete/3/'
# endpoint = 'http://127.0.0.1:8000/api/product/create'

# res = requests.get(endpoint, params={"q": "bro"}, json={"hello bro": "Bexzod"})
res = requests.delete(endpoint)
# res = requests.put(endpoint, json={"title": "Hello titljon", "content": "hello contentjon"})
print(res.status_code)
