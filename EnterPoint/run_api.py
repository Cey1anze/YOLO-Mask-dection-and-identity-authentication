import cv2
import torch

from EnterPoint import detect_api

cap = cv2.VideoCapture(0)  # 0
a = detect_api.detectapi(weights='I:\BaiduNetdiskDownload\yolov7\yolov7_mask.pt')


def run():
    with torch.no_grad():
        rec, img = cap.read()
        result, names = a.detect([img])
        img = result[0][0]  # 每一帧图片的处理结果图片
        # 每一帧图像的识别结果（可包含多个物体）
        """
        for cls, (x1, y1, x2, y2), conf in result[0][1]:
            print(names[cls], x1, y1, x2, y2, conf)  # 识别物体种类、左上角x坐标、左上角y轴坐标、右下角x轴坐标、右下角y轴坐标，置信度
            '''
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0))
                cv2.putText(img,names[cls],(x1,y1-20),cv2.FONT_HERSHEY_DUPLEX,1.5,(255,0,0))'''
        print()  # 将每一帧的结果输出分开
        """
        return img

