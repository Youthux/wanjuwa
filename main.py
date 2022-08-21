from urllib import parse
import requests
import json


def main():
    # token = 'eyJhbGciOiJIUzI1NiIbInR5cCI6IkpXVCJ9.eyJ1cGRhdGVVc2VyIjpmYWxzZSwib3BlbmlkIjoib2N0RUI1V0l4WVlNTzFFMkY4M0hTdGRkdjYxWSIsInVzZXJJZCI6MTI3MDIzLCJ1c2VyQ29kZSI6MTAzNjA0MiwidW5pb25pZCI6Im9Vam9nMVA4b1BfS1R6cDBwcEhyMzQ1M2tiaXMiLCJwaG9uZSI6bnVsbCwibmlja25hbWUiOiLog6Hov4UiLCJ1c2VyTmFtZSI6IiIsImdlbmRlciI6MSwic2VydmljZUF2YXQiOiJ1cGxvYWRzXzEvYXZhdGFyLzEwMzZfLzEwMzYwNDIuanBnIiwibGFzdFVwZGF0ZUF2YXQiOiJodHRwczovL3RoaXJkd3gucWxvZ28uY24vbW1vcGVuL3ZpXzMyLzJVQ1FFUXRYcGthU0piREkwblhQR1d2ekhpYzZpY2UxdlczRG9oRDhSVXAwem1UMmwwdWxkQ0RxcFR4eUNjRm9uVXRjaGVoWFhqTXRTTk84TDM2ZGVkQncvMCIsImF2YXRhcnVybCI6Imh0dHBzOi8vd3d3Lndhbmp1d293LmNvbS9zaG9wL3VwbG9hZHNfMS9hdmF0YXIvMTAzNl8vMTAzNjA0Mi5qcGciLCJyZWFsQXJlYSI6IiIsInJlYWxDaXR5IjoiIiwicmVhbFByb3ZpbmNlIjoiIiwicmVhbENvdW50cnkiOiIiLCJjaXR5Q29kZSI6NDQwMzAwLCJhY3RpdmVDbGFzc2lmeSI6MSwiYWN0aXZlUGFyYW1zIjoie1wiY2xhc3NpZnlfMVwiOlt7XCJpZFwiOjEwMDEsXCJuYW1lXCI6XCLnvr3mr5vnkINcIixcImNsYXNzaWZ5XCI6MSxcInNlYXJjaFwiOntcImF0eXBlc0NsYXNzaWZ5XCI6MSxcImF0eXBlc1R5cGVcIjoxMDAxfSxcInhjaGVja1wiOmZhbHNlfV19IiwiYmlydGhkYXkiOiIiLCJ0cmFpdCI6IiIsImhvYmJ5IjoiIiwiYmxhY2tDb3VudCI6MCwiYmVCbGFja0NvdW50Ijo2LCJmYW5zQ291bnQiOjAsImZvbGxvd0NvdW50IjoyLCJmcmllbmRDb3VudCI6MCwiZG9tYWluIjoiaHR0cHM6Ly93d3cud2FuanV3b3cuY29tL3Nob3AvIiwiaWF0IjoxNjYxMDY3NDQ2LCJleHAiOjE2NjEwNzQ2NDZ9.Y2pymlwdOHk56Cqm3uTW3WJPiJAbHByEWcjvZdn6ctc'
    token = input("请输入token:")
    user_id = input("请输入用户ID:")

    # 最近的rows场羽毛球活动
    rows = 1000
    # 深圳地区代码
    city_code = 440300
    # 是否查询到
    flag = False

    activities = get_activity_list(token, rows, city_code)
    for activity in activities["data"]:
        article_id = activity["actId"]
        users = get_user_list(token, article_id, city_code)
        for user in users["data"]["signUps"]:
            user_code = user["userCode"]
            if user_id == str(user_code):
                print("查询到该用户报名了活动：" + activity["actTitle"])
                flag = True
                break
    if not flag:
        print("未查询到该用户报名了任何活动")


def get_activity_list(token, rows, city_code):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': token
    }
    get_activity_param = {"page": 1,
                          "row": 10,
                          "isReach": "true",
                          "mainType": 1,
                          "classify": "[{\"atypesClassify\":1,\"atypesType\":1001}]",
                          "latitude": 22.53332,
                          "longitude": 113.93041,
                          "rows": rows,
                          "cityCode": city_code,
                          "pageRoute": "pages/home/home"}

    get_activity_data = parse.urlencode(get_activity_param)
    get_activity_url = "https://www.wanjuwow.com/shop/active/list2"

    response = requests.post(url=get_activity_url, headers=headers, data=get_activity_data)
    result = json.loads(response.text, strict=False)
    print(response.text)
    return result


def get_user_list(token, article_id, city_code):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': token
    }
    get_user_param = {"articleId": article_id, "cityCode": city_code,
                      "pageRoute": "pages/active/signup/listShow/listShow"}
    get_user_data = parse.urlencode(get_user_param)
    get_user_url = "https://www.wanjuwow.com/shop/signUp2/userList"

    response = requests.post(url=get_user_url, headers=headers, data=get_user_data)
    result = json.loads(response.text, strict=False)
    return result


if __name__ == "__main__":
    main()
