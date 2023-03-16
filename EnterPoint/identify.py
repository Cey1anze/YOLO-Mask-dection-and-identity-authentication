import base64
import os

import requests
import json

API_KEY = "bifSN35Mu84ON7LGm5xlc9RT"
SECRET_KEY = "h0kx9fuIX1Zz8itGKsq8qKrL4R3POIPw"


def img_data(img1Path, img2Path):
    # 把图片转换成base64编码
    f = open(r'%s' % img1Path, 'rb')
    pic1 = base64.b64encode(f.read())
    f.close()
    f = open(r'%s' % img2Path, 'rb')
    pic2 = base64.b64encode(f.read())
    f.close()
    # 将文件转化为可提交信息
    params = json.dumps(
        [{"image": str(pic1, 'utf-8'), "image_type": "BASE64", "face_type": "LIVE", "quality_control": "NONE"},
         {"image": str(pic2, 'utf-8'), "image_type": "BASE64", "face_type": "LIVE", "quality_control": "NONE"}]
    )
    return params.encode(encoding='UTF8')


def main():
    url = "https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=" + get_access_token()

    # 图片路径列表
    # TODO 接入摄像头，实时获取图片进行身份对比识别，将已知身份图片存入验证库
    img_paths = ['pic5.jpg', 'IMG_3122.jpg', '20190111144903263.jpg', 'pic5_nomask.jpg']

    for i in range(1, len(img_paths)):
        # 将第i张图片与pic1进行对比
        payload = img_data('pic5.jpg', img_paths[i])
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(f"比对结果（pic1与{img_paths[i]}）：{response.text}")


# TODO 新增验证方法，main函数返回的结果进行判断，如果是同一个人则返回True，否则返回False，通过可视化界面交互

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    main()