import requests

URL = ""

def test_server():
  res = requests.get(URL + '/alive')
  assert(r.status_code == 200)
