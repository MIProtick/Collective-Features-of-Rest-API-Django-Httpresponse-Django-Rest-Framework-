import json
import requests

ENDPOINT = 'http://127.0.0.1:8000/api/status/'


def make_api_call(method='get', data={}, id=None, make_json=True):
    headers = {'content-type': 'text/plain'}
    if make_json:
        data = json.dumps(data)
        headers['content-type'] = 'application/json'
        
    if id is None:
        resp = requests.request(method, ENDPOINT, data=data, headers=headers)
        print(resp.text)
        print(resp.status_code)
        
    else:
        resp = requests.request(method, f'{ENDPOINT}?id={id}', data=data, headers=headers)
        print(resp.text)
        print(resp.status_code)
        

# make_api_call()
# make_api_call(data={'id': 3})
# make_api_call(data={'id': 3}, id=4)

# make_api_call(method='post', data={'user': 1, 'content': 'test api content again'})
# make_api_call(method='put', data={'id': 6, 'user': 1, 'content': 'test api content update by put'})
# make_api_call(method='patch', data={'id': 6, 'content': 'test api content update by patch'})
# make_api_call(method='delete', data={'id': 6})
