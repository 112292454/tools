import requests


def curl_basic(url):
    try:
        # 发送HTTP GET请求
        response = requests.get(url)

        # 检查响应状态码
        if response.status_code == 200:
            # 输出网页内容
            print(response.text)
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
