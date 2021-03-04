# -*- coding: utf-8 -*-
# @Time : 2021/2/8 10:26
# @Author : Zhining Zhang
# @site :  
# @File : cat_dog.py
# @main : 猫狗分类
# @Software: PyCharm
from keras.preprocessing.image import ImageDataGenerator;
from keras import layers
from keras import models
from keras import optimizers
import time
import Dense_all_link.mapping_training_process as  mtp
'''
数据预处理
(1) 读取图像文件。
(2) 将 JPEG 文件解码为 RGB 像素网格。
(3) 将这些像素网格转换为浮点数张量。
(4) 将像素值（0~255 范围内）缩放到 [0, 1] 区间（正如你所知，神经网络喜欢处理较小的输
入值）
'''
def readImage():
    # 进行图像预处理
    '''
     rescale进行图像预处理，将所有图像乘以 1/255 缩放
     rotation_range 是角度值（在 0~180 范围内），表示图像随机旋转的角度范围。
     width_shift 和 height_shift 是图像在水平或垂直方向上平移的范围（相对于总宽度或总高度的比例）。
     shear_range 是随机错切变换的角度。
     zoom_range 是图像随机缩放的范围。
     horizontal_flip 是随机将一半图像水平翻转。如果没有水平不对称的假设（比如真实世界的图像），这种做法是有意义的。
     fill_mode 是用于填充新创建像素的方法，这些新像素可能来自于旋转或宽度/高度平移。
    :return:
    '''
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

    # 转为张量
    # 转为张量
    train_generator = datagen.flow_from_directory(
        'D:\\贵州大学\\数据集\\dogs-vs-cats\\train\\test',
        target_size=(150,150),#将所有图像的大小调整为 150×150
        batch_size=20,
        class_mode='binary'#因为使用了 binary_crossentropy损失，所以需要用二进制标签
    )

    validation_generator = datagen.flow_from_directory(
        'D:\\贵州大学\\数据集\\dogs-vs-cats\\train\\test1',
        target_size=(150, 150),  # 将所有图像的大小调整为 150×150
        batch_size=20,
        class_mode='binary'  # 因为使用了 binary_crossentropy损失，所以需要用二进制标签
    )
    print(validation_generator)
    return train_generator,validation_generator

def modelCreate(train_generator,validation_generator):
    """
    模型创建
    :param train_generator: 训练集和测试集
    :param validation_generator:
    :return:模型训练结果
    """
    '''
    由于这里要处理的是更大的图像和更复杂的问题，你需要相应地增大网络，即再增加一个 Conv2D + MaxPooling2D 的组合。
    这既可以增大网络容量，也可以进一步减小特征图的尺寸，使其在连接 Flatten 层时尺寸不会太大。
    本例中初始输入的尺寸为 150×150（有些随意的选择），所以最后在 Flatten 层之前的特征图大小为 7×7。
     网络中特征图的深度在逐渐增大（从 32 增大到 128），而特征图的尺寸在逐渐减小（从150×150 减小到 7×7）。
     这几乎是所有卷积神经网络的模式。
    '''
    model = models.Sequential()
    # 2D卷积
    model.add(layers.Conv2D(32, (3, 3), activation='relu',
                            input_shape=(150, 150, 3)))
    # 在每个 MaxPooling2D 层之后，特征图的尺寸都会减半
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    # 为了进一步降低过拟合，你还需要向模型中添加一个 Dropout 层，添加到密集连接分类器之前
    # Dropout解决过拟合
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    print(model.summary())
    model.compile(loss='binary_crossentropy',
        optimizer=optimizers.RMSprop(lr=1e-4),
        metrics=['acc'])
    history = model.fit_generator(
        train_generator,
        steps_per_epoch=100,
        epochs=30,
        max_queue_size=2048,
        validation_data=validation_generator,
        validation_steps=50)
    print(history)
    # 保存模型
    model.save('cats_and_dogs_small_2.h5')
    return history.history
if __name__=="__main__":
    start_time = time.time();
    train_generator,validation_generator = readImage();
    history_dict = modelCreate(train_generator,validation_generator)
    end_time = time.time();
    mtp.mappingLoss(history_dict)
    mtp.mappingAcc(history_dict)

    print(end_time-start_time)