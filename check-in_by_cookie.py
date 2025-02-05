import time

import requests

website_cookies_pairs = {
    'https://glados.space/api/user/checkin': {
        '_ga': 'GA1.1.1994312165.1725023641',
        '_ga_CZFVKMNT9J': 'GS1.1.1725023640.1.1.1725023667.0.0.0',
        'koa:sess': 'eyJ1c2VySWQiOjUzMDgwNSwiX2V4cGlyZSI6MTc1MDk0MzY2Nzc1OCwiX21heEFnZSI6MjU5MjAwMDAwMDB9',
        'koa:sess.sig': 'GluBnMtC9qsHnrz_j7QY025L2mQ'
    },
    'https://www.sexyai.top/api/user/sign-in': {
        'cf_clearance': 'YUG2HGymDOuODUjtme6vUf4FRFYRdd56ocPW7zaf1OU-1738779028-1.2.1.1-zs6wRRj_bgPNcQN0uiCp_B9k8tP3CwY3ZDU5nhY0wFqMslZHDJpNYtZpSmQ0SntTWFfYyQnHPh3iNjaFrtil866Fju0pNB1CKhf3TkRc3THUxT.EiX6_4scVMP5_4zBdanB_pRxzphAxoFGhqisKhZY0T39PyV87mbfUXHEIrYaxypwXJEp8pGkUbAliFWjicy5KSTrEXO11P62w5mV8YHq00v3kH.wmGus3LNpZV_xJFGUKuaGfoNS2R4LizMKO1FuCPTCErFelUOvjh.TOh7J8sRzUH_SyTXIr23mplpg',
        'g_state': '{"i_l":0}'
    },
    'https://www.jqmcy.net/wp-json/b2/v1/userMission': {
        '': '__51uvsct__JzlfA6Ceb6XkEZjb=1; __51vcke__JzlfA6Ceb6XkEZjb=6839ac76-dd01-54ca-9b74-bae8e9586386; __51vuft__JzlfA6Ceb6XkEZjb=1738777239979; 5ec916ef4b27483d881ec60c5ccc81cd=7398bd474320c386297938c5f135154a; X_CACHE_KEY=fb70dacab943c7b80a18c23b352fb22a; _ga=GA1.1.1034956797.1738777242; _clck=zrtjkb%7C2%7Cft6%7C0%7C1862; gg_info=1738777245; b097ccc50f1fd60f2425116eabe06f9d=ca25aa5b422bb2e53b01c066bdc0db69; b2_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3LmpxbWN5Lm5ldCIsImlhdCI6MTczODc3ODA3NCwibmJmIjoxNzM4Nzc4MDc0LCJleHAiOjE3Mzk5ODc2NzQsImRhdGEiOnsidXNlciI6eyJpZCI6IjI3MTA2In19fQ.U3Q6AsuzQmnL3HyTg4v81_vX-JQDWinOx09q8il-pDA; wordpress_logged_in_1ac2ef818e3150718c06ed69957562b1=user27106_446%7C1739339674%7CXZ44hCRgbZH3jPfBwiiq0cMMKuzagX4HNeNnpjAS2R0%7C6abca32da36bccb160ce63fa52f11011f0ee8c79b0119b8f8a9fbe1bec68b79b; __vtins__JzlfA6Ceb6XkEZjb=%7B%22sid%22%3A%20%226d9de58e-ace0-5968-b2f8-913cdc247932%22%2C%20%22vd%22%3A%2021%2C%20%22stt%22%3A%20838942%2C%20%22dr%22%3A%2093384%2C%20%22expires%22%3A%201738779878918%2C%20%22ct%22%3A%201738778078918%7D; _ga_0XF072HTS6=GS1.1.1738777241.1.1.1738778078.60.0.0; PHPSESSID=13541emdq4ogtsj6sc1qgfha5f; _clsk=10d6987%7C1738778093023%7C1%7C1%7Cj.clarity.ms%2Fcollect'
    }

}

website_payload_pairs = {
    'https://glados.space/api/user/checkin': {'token': 'glados.one'},

}

website_headers_pairs = {
    'https://www.sexyai.top/api/user/sign-in': {
        'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3Mzg3NzkwNzksImV4cCI6MTc0MTM3MTA3OSwiVUlEIjo1MDQ3N30.CKrYZ6o_T-y6PQX8me0lLvwSYKOqJfyVmssRXIxjkFs'
    },
    'https://www.jqmcy.net/wp-json/b2/v1/userMission': {
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3LmpxbWN5Lm5ldCIsImlhdCI6MTczODc3ODA3NCwibmJmIjoxNzM4Nzc4MDc0LCJleHAiOjE3Mzk5ODc2NzQsImRhdGEiOnsidXNlciI6eyJpZCI6IjI3MTA2In19fQ.U3Q6AsuzQmnL3HyTg4v81_vX-JQDWinOx09q8il-pDA'
    }
}

need_proxies = [
    'https://www.sexyai.top/api/user/sign-in',
]


proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}


# payload = json.dumps({'token': 'glados.one'})


# 将字典格式化为 Cookie 字符串

def format_cookies(cookies):
    # 如果仅由一个键值对组成，且key为空，则直接返回value。说明是直接从浏览器复制的 Cookie 字符串
    if len(cookies) == 1 and '' in cookies:
        return cookies['']
    return '; '.join([f'{key}={value}' for key, value in cookies.items()])


# 定义发送请求的函数
def send_checkin_request(url, headers, payload):
    try:
        print('Sending check-in request to:', url)
        if url in need_proxies:
            response = requests.post(url, headers=headers, json=payload, proxies=proxies)
        else:
            response = requests.post(url, headers=headers, json=payload)
        print('Check-in Status Code:', response.status_code)
        print('Check-in Response:', response.json())
        print('Check-in Time:', time.ctime())
    except Exception as e:
        print('An error occurred:', e)


# 主循环，每隔 3 小时发送一次请求
while True:
    for website, cookies in website_cookies_pairs.items():
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8'
        }
        if website in website_headers_pairs:
            headers.update(website_headers_pairs[website])
        formatted_cookies = format_cookies(cookies)
        headers['Cookie'] = formatted_cookies

        url = website
        payload = website_payload_pairs[website] if website in website_payload_pairs else ''
        send_checkin_request(url, headers, payload)
    time.sleep(3 * 60 * 60)  # 3 hours in seconds
