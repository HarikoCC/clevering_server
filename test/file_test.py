import requests
from datetime import datetime

BASE_URL = "http://localhost:8000/file"

# 假设你已经有了一个有效的uid和token
UID = 1
TOKEN = "your_valid_token_here"  # 替换为实际的token

# 测试根据用户id查询文件列表
def test_list(uid, token):
    url = f"{BASE_URL}/list"
    params = {"uid": uid, "token": token}
    response = requests.get(url, headers={}, params=params)
    print(f"List URL: {url}")
    print(f"List Params: {params}")
    print(f"List Status Code: {response.status_code}")
    try:
        print("List Response:", response.json())
    except ValueError as e:
        print("List Response is not valid JSON:", response.text)

# 测试根据文件名查询文件列表
def test_listname(fname, token):
    url = f"{BASE_URL}/listname"
    params = {"fname": fname, "token": token}
    response = requests.get(url, headers={}, params=params)
    print(f"ListName URL: {url}")
    print(f"ListName Params: {params}")
    print(f"ListName Status Code: {response.status_code}")
    try:
        print("ListName Response:", response.json())
    except ValueError as e:
        print("ListName Response is not valid JSON:", response.text)

# 测试显示所有文件列表
def test_listall(token):
    url = f"{BASE_URL}/listall"
    params = {"token": token}
    response = requests.get(url, headers={}, params=params)
    print(f"ListAll URL: {url}")
    print(f"ListAll Params: {params}")
    print(f"ListAll Status Code: {response.status_code}")
    try:
        print("ListAll Response:", response.json())
    except ValueError as e:
        print("ListAll Response is not valid JSON:", response.text)

# 测试创建新文件
def test_create(uid, token, file_path):
    url = f"{BASE_URL}/create"
    params = {"uid": uid, "token": token}
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, headers={}, params=params, files=files)
    print(f"Create URL: {url}")
    print(f"Create Params: {params}")
    print(f"Create Files: {file_path}")
    print(f"Create Status Code: {response.status_code}")
    try:
        print("Create Response:", response.json())
    except ValueError as e:
        print("Create Response is not valid JSON:", response.text)

# 测试删除文件
def test_delete(fid, token):
    url = f"{BASE_URL}/delete"
    params = {"fid": fid, "token": token}
    response = requests.post(url, headers={}, params=params)
    print(f"Delete URL: {url}")
    print(f"Delete Params: {params}")
    print(f"Delete Status Code: {response.status_code}")
    try:
        print("Delete Response:", response.json())
    except ValueError as e:
        print("Delete Response is not valid JSON:", response.text)

# 测试更新文件
def test_update(fid, token, file_path):
    url = f"{BASE_URL}/update"
    params = {"fid": fid, "token": token}
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, headers={}, params=params, files=files)
    print(f"Update URL: {url}")
    print(f"Update Params: {params}")
    print(f"Update Files: {file_path}")
    print(f"Update Status Code: {response.status_code}")
    try:
        print("Update Response:", response.json())
    except ValueError as e:
        print("Update Response is not valid JSON:", response.text)

# 测试下载文件
def test_download(fid, token):
    url = f"{BASE_URL}/download"
    params = {"fid": fid, "token": token}
    response = requests.post(url, headers={}, params=params)
    print(f"Download URL: {url}")
    print(f"Download Params: {params}")
    print(f"Download Status Code: {response.status_code}")
    if response.status_code == 200:
        with open(f"downloaded_{datetime.now().strftime('%Y%m%d%H%M%S')}_{fid}", "wb") as f:
            f.write(response.content)
        print("Downloaded file saved successfully.")
    else:
        try:
            print("Download Response:", response.json())
        except ValueError as e:
            print("Download Response is not valid JSON:", response.text)

if __name__ == "__main__":
    # 测试创建新文件
    test_create(UID, TOKEN, "test.txt")
    print("\n")
    input("press enter to delete")


    # 测试根据用户id查询文件列表
    test_list(UID, TOKEN)
    print("\n")
    input("press enter to delete")

    # 测试根据文件名查询文件列表
    test_listname("example.txt", TOKEN)
    print("\n")
    input("press enter to delete")

    # 测试显示所有文件列表
    test_listall(TOKEN)


    FILE_ID = 1

    # 测试更新文件
    test_update(FILE_ID, TOKEN, "path/to/updated_example.txt")
    print("\n")
    input("press enter to delete")

    # 测试下载文件
    test_download(FILE_ID, TOKEN)
    print("\n")
    input("press enter to delete")

    # 测试删除文件
    test_delete(FILE_ID, TOKEN)
    print("\n")
    input("press enter to delete")
