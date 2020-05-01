import os
from requests import get

print(os.path.abspath('test.json'))
'/Users/alekseyostrovskiy/Desktop/sigamebot/games/test.json'

print(get('http://localhost:5000/api/v2/packs/1').json())
