import json
import requests

ENDPOINT = 'http://127.0.0.1:8000/api/status/'
AUTH_ENDPOINT = 'http://127.0.0.1:8000/api/auth/'
REG_ENDPOINT = 'http://127.0.0.1:8000/api/auth/register/'

IMAGE_PATH = '/media/protick/MyResources1/MyProjects/Django/rest_api_skeleton/im01.png'


auth_data = {
    'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6InByb3RpY2s4IiwiZXhwIjoxNjM0MTg3MzE5LCJlbWFpbCI6InByb3RpY2s4QGdtYWlsLmNvbSJ9.nrCHaVR6lgAf7IKUQfdS-UQXznxNO1KGgU7t_1Bz_FE'
}


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
        resp = requests.request(
            method, f'{ENDPOINT}?id={id}', data=data, headers=headers)
        print(resp.text)
        print(resp.status_code)


# make_api_call()
# make_api_call(data={'id': 3})
# make_api_call(data={'id': 3}, id=4)

# make_api_call(method='post', data={'user': 1, 'content': 'test api content again'})
# make_api_call(method='put', data={'id': 6, 'user': 1, 'content': 'test api content update by put'})
# make_api_call(method='patch', data={'id': 6, 'content': 'test api content update by patch'})
# make_api_call(method='delete', data={'id': 6})


def get_token():
    global auth_data
    headers = {
        'Content-Type': 'application/json'
    }
    resp = requests.post(AUTH_ENDPOINT, data=json.dumps(
        {"username": "protick", "password": "protick"}), headers=headers)
    auth_data = resp.json()
    return auth_data


def test_api(id=None, post_data=None, put_data=None, headers={}, doDelete=False, files=None):

    if id is not None:
        r_detail = requests.get(f'{ENDPOINT}{id}/', headers=headers)
        print('detail: ', r_detail.text, '\n')

        if put_data is not None:
            r_put = requests.put(f'{ENDPOINT}{id}/',
                                 data=put_data, headers=headers)
            print('update: ', r_put.text, '\n')

        if doDelete:
            r_del = requests.delete(f'{ENDPOINT}{id}/', headers=headers)
            print('delete: ', r_del.status_code)
            print('delete: ', r_del.text)

    else:
        r_list = requests.get(ENDPOINT)
        print('list: ', r_list.text, '\n')

        if post_data is not None:
            if files is not None:
                r_post = requests.post(
                    ENDPOINT, data=post_data, headers=headers, files=files)
            else:
                r_post = requests.post(
                    ENDPOINT, data=post_data, headers=headers)

            print('post: ', r_post.text, '\n')

# # token
# print(get_token())


post_headers = {
    'content-type': 'application/json',
    'Authorization': 'Token ' + auth_data['token']
}

# # 1 list
# test_api()

# # 2 list + post
# with open(IMAGE_PATH, 'rb') as image:
#     image_data = {'image':image }

#     post_headers = {
#         'content-type': 'application/json',
#         'Authorization': 'Token ' + auth_data['token']
#     }
#     post_headers_files = {
#         'Authorization': 'Token ' + auth_data['token']
#     }
#     test_api(
#         post_data = {'content': 'Complete test post'},
#         headers = post_headers,
#     )

#     test_api(
#         post_data = {'content': 'Complete test post'},
#         headers = post_headers_files,
#         files=image_data
#     )

# # 3 put
# test_api(id=9, put_data=json.dumps({'content': 'Complete test update'}), headers=post_headers)

# # 3 put
# test_api(id=9, headers=post_headers, doDelete=True)


# Authentication to account
post_headers_files = {
    'Authorization': 'Token ' + auth_data['token']
}

# # Authentication
# resp = requests.post(AUTH_ENDPOINT, data={'username': 'protick', 'password': 'protick'})
# print(resp.text)

# Registration
resp = requests.post(REG_ENDPOINT, data={'username': 'protick9', 'password': 'protick9', 'password2': 'protick9', 'email': 'protick9@gmail.com' }, headers=post_headers)
print(resp.text)
