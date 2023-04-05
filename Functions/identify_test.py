import asyncio
import base64
import json
import time

import cv2
import face_recognition

from Qt.UserHolder import UserHolder
from Qt.sqlUtils import sqlUtils

user_json = json.loads(sqlUtils.search_face_information())  # 原始数据库json内容
photo_list = []
name_list = []
decoded_photo_list = []


def get_faces_base64_from_database():
    photo_list.clear()
    name_list.clear()
    for username, data in user_json.items():
        if data[2] is not None:
            photo_list.append(data[2])
            name_list.append(data[1])
    return photo_list, name_list


def auto_identify(frame):
    # 循环数
    count = 0
    # 如果检测到人脸，则保存当前帧为JPEG格式文件
    cv2.imwrite("img1.jpg", frame)
    # 加载检测到的人脸图片
    unknown_image = face_recognition.load_image_file("img1.jpg")

    # 将检测到的人脸编码为128维向量
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    for i in range(len(get_faces_base64_from_database()[0])):
        # 解码图片
        imgdata = base64.b64decode(get_faces_base64_from_database()[0][i])
        # 将图片保存为文件
        with open("img3.jpg", 'wb') as f:
            f.write(imgdata)
        # 加载本地图片
        known_image = face_recognition.load_image_file("img3.jpg")

        # 将本地图片编码为128维向量
        known_encoding = face_recognition.face_encodings(known_image)[0]

        # 计算两张图片的欧氏距离，判断是否为同一个人
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)

        if results[0]:
            return f"检测为：{get_faces_base64_from_database()[1][i]}"
        else:
            count += 1

    if count == len(get_faces_base64_from_database()[0]):
        count = 0
        return "数据库中无结果"


def main():
    cap = cv2.VideoCapture(0)

    # 记录上一次执行的时间
    last_time = time.time()

    # 开始视频流循环
    while True:
        # 读取一帧视频流
        ret, frame = cap.read()
        if not ret:
            break

        # 进行人脸检测和身份认证
        # 只在距离上次执行超过5秒时才执行
        if time.time() - last_time >= 5:
            # 转换为灰度图像
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 检测人脸
            faces = face_recognition.face_locations(gray)
            if len(faces) > 0:
                print(auto_identify(frame))

            last_time = time.time()  # 更新上一次执行的时间

        # 按下 q 键退出循环
        if cv2.waitKey(1) == ord('q'):
            break

    # 释放视频流和窗口资源
    cap.release()
    cv2.destroyAllWindows()
