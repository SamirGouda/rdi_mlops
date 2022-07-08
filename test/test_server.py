import os
import sys

sys.path.append(os.getcwd())
from flask_api import app

def test_alive():
  with app.test_client() as c:
    res = c.get('/alive')
    res_code = res.status_code
    assert(res_code == 200)
     
if __name__ == "__main__":
    test_alive()
