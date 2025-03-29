import requests

BASE_URL = "http://localhost:8000/user"

# 测试用户注册
def test_signup():
    url = f"{BASE_URL}/signup"
    payload = {
        "user_id": 1,
        "user_name": "test_user",
        "user_type": 1,
        "user_phone": "1234567890",  # 改为字符串
        "user_password": "password123"
    }
    response = requests.post(url, json=payload)
    print(f"Signup URL: {url}")
    print(f"Signup Payload: {payload}")
    print(f"Signup Status Code: {response.status_code}")
    try:
        print("Signup Response:", response.json())
    except ValueError as e:
        print("Signup Response is not valid JSON:", response.text)

# 测试用户登录
def test_signin():
    url = f"{BASE_URL}/signin"
    payload = {
        "sign_in_mode": 0,
        "user_info": 1,
        "user_password": "password123"
    }
    response = requests.post(url, json=payload)
    print(f"Signin URL: {url}")
    print(f"Signin Payload: {payload}")
    print(f"Signin Status Code: {response.status_code}")
    try:
        response_json = response.json()
        print("Signin Response:", response_json)
        return response_json.get('data')  # 返回token供后续使用
    except ValueError as e:
        print("Signin Response is not valid JSON:", response.text)
        return None

# 测试获取用户信息
def test_info(uid, token):
    params = {"uid": uid, "token": token}
    url = f"{BASE_URL}/info"
    response = requests.get(url, params=params)
    print(f"Info URL: {url}")
    print(f"Info Params: {params}")
    print(f"Info Status Code: {response.status_code}")
    try:
        print("Info Response:", response.json())
    except ValueError as e:
        print("Info Response is not valid JSON:", response.text)

# 测试更新用户信息
def test_update(uid, token):
    headers = {}
    params = {"uid": uid, "token": token}
    url = f"{BASE_URL}/update"
    payload = {
        "user_id": uid,
        "user_name": "updated_test_user",
        "user_type": 2,
        "user_phone": "0987654321",  # 改为字符串
        "user_password": "new_password123"
    }
    response = requests.post(url, headers=headers, params=params, json=payload)
    print(f"Update URL: {url}")
    print(f"Update Params: {params}")
    print(f"Update Payload: {payload}")
    print(f"Update Status Code: {response.status_code}")
    try:
        print("Update Response:", response.json())
    except ValueError as e:
        print("Update Response is not valid JSON:", response.text)

# 测试删除用户
def test_delete(uid, token):
    headers = {}
    params = {"uid": uid, "token": token}
    url = f"{BASE_URL}/delete"
    payload = {
        "user_id": uid,
        "user_password": "new_password123"
    }
    response = requests.post(url, headers=headers, params=params, json=payload)
    print(f"Delete URL: {url}")
    print(f"Delete Params: {params}")
    print(f"Delete Payload: {payload}")
    print(f"Delete Status Code: {response.status_code}")
    try:
        print("Delete Response:", response.json())
    except ValueError as e:
        print("Delete Response is not valid JSON:", response.text)

if __name__ == "__main__":
    test_signup()
    print("\n")

    token = test_signin()
    print("\n")
    if token:
        test_info(1, token)
        print("\n")

        test_update(1, token)
        print("\n")

        test_delete(1, token)