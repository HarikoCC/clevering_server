import requests
from datetime import datetime

BASE_URL = "http://localhost:8000/status"

# 测试更新状态并添加日志
def test_update(uid, token):
    url = f"{BASE_URL}/update"
    payload = {
        "user_id": uid,
        "heart_rate": 75,
        "hrv": 45,
        "blood_oxygen": 98,
        "concentration": 85
    }
    params = {"uid": uid, "token": token}
    response = requests.post(url, headers={}, params=params, json=payload)
    print(f"Update URL: {url}")
    print(f"Update Params: {params}")
    print(f"Update Payload: {payload}")
    print(f"Update Status Code: {response.status_code}")
    try:
        print("Update Response:", response.json())
    except ValueError as e:
        print("Update Response is not valid JSON:", response.text)

# 测试获取用户最新状态
def test_status(uid, token):
    url = f"{BASE_URL}/status"
    params = {"uid": uid, "token": token}
    response = requests.get(url, headers={}, params=params)
    print(f"Status URL: {url}")
    print(f"Status Params: {params}")
    print(f"Status Status Code: {response.status_code}")
    try:
        print("Status Response:", response.json())
    except ValueError as e:
        print("Status Response is not valid JSON:", response.text)

# 测试根据id获取用户日志
def test_record(uid, token, start_time, end_time):
    url = f"{BASE_URL}/record"
    if start_time and end_time:
        mode = 0
        payload = {
            "mode": mode,
            "user_id": uid,
            "start_time": start_time,
            "end_time": end_time
        }
    else:
        mode = 0
        payload = {
            "mode": mode,
            "user_id": uid
        }
    params = {"uid": uid, "token": token}
    response = requests.get(url, headers={}, params=params, json=payload)
    print(f"Record URL: {url}")
    print(f"Record Params: {params}")
    print(f"Record Payload: {payload}")
    print(f"Record Status Code: {response.status_code}")
    try:
        print("Record Response:", response.json())
    except ValueError as e:
        print("Record Response is not valid JSON:", response.text)


# 测试根据日期删除用户状态日志
def test_delete(uid, token, start_time=None, end_time=None):
    url = f"{BASE_URL}/delete"
    if start_time and end_time:
        mode = 0
        payload = {
            "mode": mode,
            "user_id": uid,
            "start_time": start_time,
            "end_time": end_time
        }
    else:
        mode = 0
        payload = {
            "mode": mode,
            "user_id": uid
        }
    params = {"uid": uid, "token": token}
    response = requests.post(url, headers={}, params=params, json=payload)
    print(f"Delete URL: {url}")
    print(f"Delete Params: {params}")
    print(f"Delete Payload: {payload}")
    print(f"Delete Status Code: {response.status_code}")
    try:
        print("Delete Response:", response.json())
    except ValueError as e:
        print("Delete Response is not valid JSON:", response.text)

if __name__ == "__main__":
    # 假设你已经有了一个有效的uid和token
    uid = 1
    token = "abb1d3f7-5207-4b01-87da-1ab2455c0e9f"  # 替换为实际的token

    # 测试更新状态并添加日志
    test_update(uid, token)
    print("\n")


    # 测试获取用户最新状态
    test_status(uid, token)
    print("\n")

    start_time = "2023-03-29 20:49:06"
    end_time = "2024-03-29 20:49:06"
    # 测试根据id获取用户日志（全部记录）
    test_record(uid, token,start_time, end_time)
    print("\n")


    # 测试根据日期获取用户日志

    test_record(uid, token, start_time, end_time)
    print("\n")
    input("press enter to delete")

    # 测试根据日期删除用户状态日志
    test_delete(uid, token, start_time, end_time)
    print("\n")

    # 测试根据id删除用户状态日志（全部记录）
    test_delete(uid, token,start_time, end_time)
