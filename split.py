import os

# 定义路径
mask_dir = './mask'
train_images_dir = os.path.join(mask_dir, 'images', 'train')

val_images_dir = os.path.join(mask_dir, 'images', 'val')

train_txt_path = os.path.join(mask_dir, 'train.txt')
val_txt_path = os.path.join(mask_dir, 'val.txt')

# 获取训练集图片和对应标签文件的路径
train_image_paths = [os.path.join(train_images_dir, filename) for filename in os.listdir(train_images_dir)]


# 将训练集图片和对应标签文件的路径写入train.txt文件
with open(train_txt_path, 'w') as f:
    for image_path in train_image_paths:
        f.write(image_path + '\n')

# 获取验证集图片和对应标签文件的路径
val_image_paths = [os.path.join(val_images_dir, filename) for filename in os.listdir(val_images_dir)]


# 将验证集图片和对应标签文件的路径写入val.txt文件
with open(val_txt_path, 'w') as f:
    for image_path in val_image_paths:
        f.write(image_path + '\n')