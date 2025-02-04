import json

import requests
import time

website_cookies_pairs = {
    'https://glados.space/api/user/checkin': {
        '_ga': 'GA1.1.1994312165.1725023641',
        '_ga_CZFVKMNT9J': 'GS1.1.1725023640.1.1.1725023667.0.0.0',
        'koa:sess': 'eyJ1c2VySWQiOjUzMDgwNSwiX2V4cGlyZSI6MTc1MDk0MzY2Nzc1OCwiX21heEFnZSI6MjU5MjAwMDAwMDB9',
        'koa:sess.sig': 'GluBnMtC9qsHnrz_j7QY025L2mQ'
    },
    'https://www.meimoai.com/api/user/sign-in': {
        'cf_clearance': 'cKHOmmQ2DJXfWTC9W4uMLfrvyX3YIrEucD6fS68JZyA-1728745938-1.2.1.1-Wy2UDjPDnOzJ9qXtgSgQbPw22xY9aDayzENRQv8_B5vzI06WT9e75vfoSvYuiOTVaJjVXIyIOOdceTHMqHFZWZrA7Z1P3lkOPCYMT3n1f.LAr78ts32kHHW_Eq.3uJs3rYa82fxHdfhaw5dAfpMFflzHRvaMYzYhoEIK.E42iwLRlfOVvvpVu.kYntscYfOsm_Wc2ddQURoD20o60TqsJuOuIJHaXVPd1bAo5_hTq2ZG15BCUsyRtTOUANJdY1VINudw.818yx2ma2TlBXMTuFqCi3iRL2F98rXzr33Jv8ZAVAL6UUUa6WzNhLeknE3S8sBbJG9uchNxQMHygmrvHNoY7yzbW7ikPO9GqDZfjFZLJssl_EqZeKr6q2T4.SSrgFHNsiva_2p3tv4CkERpJQ',
        'g_state': '{"i_l":0}'
    },

}

website_payload_pairs = {
    'https://glados.space/api/user/checkin': {'token': 'glados.one'}

    }

website_headers_pairs = {
    'https://www.meimoai.com/api/user/sign-in': {
        'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3Mjg3NDU5MDksImV4cCI6MTczMTMzNzkwOSwiVUlEIjo1MDQ3N30.-jL1gyvIfMNDljkGcbiC_FXGC5RG8AFIe6yJuTsIyxw'
    }
}

# payload = json.dumps({'token': 'glados.one'})


# 将字典格式化为 Cookie 字符串

def format_cookies(cookies):
    return '; '.join([f'{key}={value}' for key, value in cookies.items()])



# 定义发送请求的函数
def send_checkin_request(url,headers,payload):
    try:
        print('Sending check-in request to:', url)
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
