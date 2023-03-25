import base64
import os

import requests
import json

from Qt.sqlUtils import sqlUtils

API_KEY = "bifSN35Mu84ON7LGm5xlc9RT"
SECRET_KEY = "h0kx9fuIX1Zz8itGKsq8qKrL4R3POIPw"

user_json = json.loads(sqlUtils.search_face_information())  # 原始数据库json内容
otheruser_photo_list = []  # 存储除登陆用户之外的用户人脸数据


def get_otheruser_photos(now_user):
    otheruser_photo_list.clear()
    for username, data in user_json.items():
        if username != now_user and data[2] != 'None':
            otheruser_photo_list.append(data[2])
    return otheruser_photo_list


def img_data(pic1, photo):
    """Convert data to api required

    Combine the image base64 encoding into the form required by the adult face comparison api.

    Args:
        pic1(str):实时视频流图像
        photo(str):数据库中的人脸数据

    Returns:
        api所需信息
    """
    # 将文件转化为可提交信息
    params = json.dumps(
        [{"image": pic1, "image_type": "BASE64", "face_type": "LIVE", "quality_control": "NONE"},
         {"image": photo, "image_type": "BASE64", "face_type": "LIVE", "quality_control": "NONE"}]
    )
    return params.encode(encoding='UTF8')


def main(photo, now_user):
    try:
        url = "https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=" + get_access_token()

        otheruser_photo = get_otheruser_photos(now_user)
        nowUser_photo = user_json[now_user][2]

        if nowUser_photo != "None":
            payload = img_data(photo, nowUser_photo)
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)

            result = response.json()

            if result['result']['score'] < 85:

                for i in range(1, len(otheruser_photo)):
                    # 将第i张图片与pic1进行对比
                    payload = img_data(photo, otheruser_photo[i])
                    headers = {
                        'Content-Type': 'application/json'
                    }

                    response = requests.request("POST", url, headers=headers, data=payload)

                    result = response.json()

                    if result['result']['score'] > 85:
                        for username, [username, name, photo] in user_json.items():
                            if photo == result['result']['score']:
                                return str(name)

                    else:
                        return str('不与数据库中任意人脸数据匹配')
            else:
                for username, [username, name, photo] in user_json.items():
                    if photo == nowUser_photo:
                        return str(name)
        else:
            return str('数据库中暂无你的数据，请先录入人脸数据')
    except Exception as e:
        print(e)


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
