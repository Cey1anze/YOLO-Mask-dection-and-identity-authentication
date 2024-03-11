# About Mask Detection and Identification

## 目录

- 项目运行流程
  
  - 登陆 / 注册
    
  - 摄像头检测及身份识别
    
  - 上传个人信息
    
- 项目运行原理
  
  - 口罩检测
    
    - 训练模型
      
      - 预训练模型
        
      - 正式训练
        
    - 使用模型进行预测
      
      - 基础检测
        
      - 摄像头实时检测
        
  - 身份识别
    
    - 人像对比
  - 可视化界面
    
    - 建立连接

## 项目结构

```
│ 
├─Functions
│  ├─utils
│  │  └─detect_api.py
│  ├─identify.py
│  └─run_api.py
├─models
├─Qt
│  ├─Dev
│  │  ├─images
│  │  │  ├─icons
│  │  │  └─images
│  │  ├─modules
│  │  └─themes
├─utils
│  ├─aws
│  ├─google_app_engine
│  └─wandb_logging
├─detect.py
├─export.py
├─hubconf.py
├─main.py
├─requirements.txt
├─traced_model.pt
├─train.py
├─train_aux.py
├─train_mask.py
├─yolov7.pt
└─yolov7_mask.pt
```

## 项目运行流程

- 登陆 / 注册

        ![](https://cdn.jsdelivr.net/gh/HYBBWuXiDiXi/Blog_Images@main/202304011325984.png)

![](https://cdn.jsdelivr.net/gh/HYBBWuXiDiXi/Blog_Images@main/202304011326371.png)

- 主页（Need a Main LOGO pic or something else）
  
  ![](https://cdn.jsdelivr.net/gh/HYBBWuXiDiXi/Blog_Images@main/202304011329363.png)
  
- 摄像头检测（GUI Need To Be Redesign）
  
  ![](https://cdn.jsdelivr.net/gh/HYBBWuXiDiXi/Blog_Images@main/202304011340765.png)
  
- 上传个人信息（GUI Need To Be Redesign）
  
  ![](https://cdn.jsdelivr.net/gh/HYBBWuXiDiXi/Blog_Images@main/202304011342685.png)
  
- 静态图片检测（ Maybe Will Add This Function）
  

## 项目运行原理

<div align="center">
<b>口罩检测</b>
</div>

#### *Yolo算法*

    YOLO（You Only Look Once）是一种实时目标检测算法，它的主要思想是将目标检测问题转换为回归问题，使用单个神经网络预测图像中所有目标的边界框和类别。

    下面是YOLO算法的流程：

1. 输入图像：将待检测的图像输入神经网络，大小为 $448\times 448$。
  
2. 卷积神经网络：采用卷积神经网络对输入图像进行特征提取。
  
3. 边界框预测：将特征图分成 $S\times S$ 个网格（如 $7\times 7$），每个网格负责检测图像中的一部分区域。对于每个网格，预测 $B$ 个边界框（bounding box），每个边界框包含5个信息：$(x, y, w, h, confidence)$，其中 $(x, y)$ 表示边界框中心相对于当前网格左上角的偏移量，$(w, h)$ 表示边界框的宽和高，$confidence$ 表示该边界框包含目标的置信度。
  
4. 类别预测：对于每个边界框，预测目标的类别。每个边界框需要预测 $C$ 个类别的概率值，其中 $C$ 是目标类别的数量。
  
5. 边界框过滤：根据预测结果，过滤掉置信度低于阈值的边界框。通常阈值设置为0.5。
  
6. 非极大值抑制（NMS）：对于同一类别的多个边界框，采用NMS算法去除冗余的边界框，只保留重叠度最大的那个边界框。
  
7. 输出检测结果：将保留下来的边界框和对应的类别输出作为检测结果。
  

- 预训练模型

###### 1. 为什么要训练模型？

            **训练**的目的**是**让计算机程序知道“如何进行分类”

###### 2. 什么是预训练模型？

            预训练模型是指在一个大规模数据集上训练好的模型

###### 3. 为什么要预训练？

            在训练YOLO时，使用预训练模型可以提高训练效率和检测精度。这是因为预训练模型已经学习了很多通用特征，比如边缘、纹理、颜色等，可以被用于 YOLO 中的特征提取。这意味着预训练模型可以更快地收敛，因为它们已经学习了通用的图像特征，而且它们可以提供更好的初始化参数，从而使模型更容易地收敛到更好的结果。

- 正式训练
  
  正式训练使用 Yolo 官方的预训练模型 `Yolov7.pt` ，从而使训练更高效
  

###### 怎么进行训练？

1. 数据集准备：准备一个包含物体的图像和每个物体的标签的数据集。标签应该包括物体的类别和边界框的坐标。
2. 网络结构设计：选择一个适合的YOLO模型，并根据需要进行修改。
3. 模型训练：使用数据集训练YOLO模型。

**模型训练结果：**

Tip : 训练结果解读 - [Click Here](https://blog.csdn.net/m0_66447617/article/details/124180032)

> 混淆矩阵（ confusion matrix ）

![](https://cdn.jsdelivr.net/gh/HYBBWuXiDiXi/Blog_Images@main/202304011415296.png)

> P_Curve

![](https://cdn.jsdelivr.net/gh/HYBBWuXiDiXi/Blog_Images@main/202304011420817.png)

> PR_Curve

![](https://cdn.jsdelivr.net/gh/HYBBWuXiDiXi/Blog_Images@main/202304011420534.png)

> R_Curve

![](https://cdn.jsdelivr.net/gh/HYBBWuXiDiXi/Blog_Images@main/202304011420394.png)

> result

![](https://cdn.jsdelivr.net/gh/HYBBWuXiDiXi/Blog_Images@main/202304011420460.png)

> Train_batch

![](https://cdn.jsdelivr.net/gh/HYBBWuXiDiXi/Blog_Images@main/202304011420442.png)

> Test_batch

![](https://cdn.jsdelivr.net/gh/HYBBWuXiDiXi/Blog_Images@main/202304011423489.png)

- 使用模型进行预测
  
  检测过程可以分为两个步骤：网络预测和后处理。
  
      网络预测：
          在网络预测阶段，YOLO将整张图片输入卷积神经网络（CNN）中，生成一个固定大小的特征图。对于每个格子，YOLO会预测出K个边界框以及这些边界框中包含的物体的概率。每个边界框包含5个参数：x、y、w、h和物体概率。其中，x和y是边界框的中心坐标，w和h是边界框的宽度和高度，物体概率表示这个边界框中是否包含物体。
  
      后处理：
          在后处理阶段，YOLO首先会通过阈值过滤掉物体概率较低的边界框。然后，对于每个格子，选择物体概率最高的边界框作为该格子的检测结果，并将其与其他格子的检测结果进行非极大值抑制（NMS）操作，以去除重叠的检测结果。最后，YOLO将剩余的边界框转换为绝对坐标，并输出检测结果。
  
- 基础预测
  
  使用Yolo官方提供的 `Detect.py` 即可对一张照片进行预测
  
  `Detect.py` 详解：[Click Here](https://blog.csdn.net/weixin_42206075/article/details/125948887)
  
- 使用摄像头预测
  
  要在OpenCV中使用YOLO算法进行实时目标检测，需要进行以下步骤：
  
  1. 加载YOLO模型：使用OpenCV的dnn模块加载预先训练好的YOLO模型，并设置模型的参数和配置文件。
    
  2. 读取视频帧：使用OpenCV的VideoCapture模块读取视频流中的每一帧图像。
    
  3. 图像预处理：将读取到的图像进行预处理，例如缩放到模型需要的尺寸、归一化像素值等。
    
  4. 输入模型进行推理：使用OpenCV的dnn模块将预处理后的图像输入到YOLO模型中进行推理，得到目标检测结果。
    
  5. 处理检测结果：对于每个检测到的目标，将其位置和类别信息提取出来，并在图像中标注出来。
    
  6. 显示结果：将标注后的图像显示出来，可以使用OpenCV的imshow函数进行显示。
    
  7. 循环处理：重复执行2-6步骤，直到视频流结束。
    

<div align="center">
<b>身份识别</b>
</div>

#### *V1.0.0*

###### 百度云人脸对比

#### *V2.0.0*

###### Face_recognition

Face_recognition 详解 - [Click Here](https://zhuanlan.zhihu.com/p/99927894)

###### 如何进行身份识别？

- V1.0.0
  
  点击 `身份识别` 按钮，程序截取实时图像，调用百度云人脸识别接口，与数据库中存在的人脸信息进行对比
  
- V2.0.0
  
  每隔一段时间截取实时图像，使用face_recongition，与数据库中存在的人脸信息进行对比
  

<div align="center">
<b>可视化界面</b>
</div>

#### 什么是Pyside6？

    Pyside6是一个用于Python编程语言的GUI（图形用户界面）工具包，它基于Qt软件开发框架，可用于创建跨平台的桌面应用程序。Pyside6支持各种GUI元素，如按钮、文本框、标签、列表、菜单等等。

#### 怎么将可视化界面与项目的功能联系起来？

    要将GUI与功能代码连接起来，可以使用信号和槽机制。信号是GUI元素发出的事件，例如按钮被点击、复选框状态更改等。槽是处理信号的函数，例如响应按钮点击事件的函数。

#### 什么是信号和槽机制？

    信号和槽机制是一种用于在Qt和PySide6等GUI框架中连接用户界面（UI）元素和相关功能代码的方法。

    在这种机制中，UI元素（例如按钮）发出信号（例如按钮点击事件），而功能代码则包含一个或多个槽（即信号的接收器）来处理这些信号。当UI元素发出信号时，它们将被传递到相应的槽，槽将执行相关的功能代码。

    信号和槽机制的优点在于，它可以将UI和相关的功能代码分离开来，使得应用程序更易于维护和扩展。此外，由于信号和槽是完全松耦合的，因此可以在应用程序中使用它们进行高度灵活的事件处理。

    在PySide6中，可以使用QObject.connect()方法将信号与槽连接起来。在连接过程中，可以指定信号和槽的参数列表，以确保它们具有相同的参数和返回值类型。此外，可以使用disconnect()方法来解除信号和槽的连接。

```
button.clicked.connect(myFunction)
```

    在这个例子中，button是一个QPushButton对象，clicked是一个信号，myFunction是一个处理函数。当按钮被点击时，clicked信号将触发myFunction函数的执行。