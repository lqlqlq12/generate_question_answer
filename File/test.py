from tensorflow.keras.datasets import cifar10
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from typing import List
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
num_classes = 10

# load the CIFAR10 data
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# 获取维度
input_shape = x_train.shape[1:]

# 图像数据归一化，所有数值区间为0到1
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')
print('y_train shape:', y_train.shape)


def DenseNet(blocks: List, shape: tuple) -> keras.Model:
    img_input = layers.Input(shape=shape)
    x = layers.ZeroPadding2D(padding=((3, 3), (3, 3)))(img_input)
    x = layers.Conv2D(64, 7, strides=2, use_bias=False)(x)
    x = layers.BatchNormalization(axis=3, epsilon=EPSILON)(x)
    x = layers.Activation('relu')(x)
    x = layers.ZeroPadding2D(padding=((1, 1), (1, 1)))(x)
    x = layers.MaxPooling2D(3, strides=2)(x)
    x = dense_block(x, blocks[0])
    x = transition_block(x, 0.5)
    x = dense_block(x, blocks[1])
    x = transition_block(x, 0.5)
    x = dense_block(x, blocks[2])
    x = transition_block(x, 0.5)
    x = dense_block(x, blocks[3])
    x = layers.BatchNormalization(axis=3, epsilon=EPSILON)(x)
    x = layers.Activation('relu')(x)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(10, activation='softmax')(x)
    return keras.Model(img_input, x)


def conv_block(x: tf.Tensor, growth_rate) -> tf.Tensor:
    x1 = layers.BatchNormalization(axis=3, epsilon=EPSILON)(x)
    x1 = layers.Activation('relu')(x1)
    x1 = layers.Conv2D(4 * growth_rate, 1, use_bias=False)(x1)
    x1 = layers.BatchNormalization(axis=3, epsilon=EPSILON)(x1)
    x1 = layers.Activation('relu')(x1)
    x1 = layers.Conv2D(growth_rate, 3, padding="same", use_bias=False)(x1)
    x = layers.Concatenate(axis=3)([x, x1])
    return x


def dense_block(x: tf.Tensor, blocks_len: int) -> tf.Tensor:
    for i in range(blocks_len):
        x = conv_block(x, 32)
    return x

def transition_block(x: tf.Tensor, reduction: float):
    x = layers.BatchNormalization(axis=3, epsilon=EPSILON)(x)
    x = layers.Activation('relu')(x)
    x = layers.Conv2D(int(keras.backend.int_shape(x)[3] * reduction), 1, use_bias=False)(x)
    x = layers.AveragePooling2D(2, strides=2)(x)
    return x

def DenseNet41(shape: tuple) -> keras.Model:
    return DenseNet([3, 6, 6, 3], shape)

def DenseNet49(shape: tuple) -> keras.Model:
    return DenseNet([4, 6, 8, 4], shape)


num_classes = 3
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
EPSILON = 1.001e-5
EPOCHS = 10  # 训练轮数,可以根据设备情况修改大小


def train_model(model: keras.Model) -> None:
    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.SparseCategoricalCrossentropy(),
        metrics=['accuracy']
    )
    history = model.fit(x_train, y_train, epochs=EPOCHS, validation_data=(x_test, y_test))
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    print("training accuracy: {}, training loss: {}, validation accuracy: {}, validation loss: {}"
          .format(acc[-1], loss[-1], val_acc[-1], val_loss[-1]))


def evaluate_model(model: keras.Model) -> None:
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
    print("test loss: {}, test accuracy: {}".format(test_loss, test_acc))


# main
if __name__ == "__main__":
    model_41 = DenseNet41(shape=input_shape)
    train_model(model_41)
    model_49 = DenseNet49(shape=input_shape)
    train_model(model_49)

    evaluate_model(model_41)
    evaluate_model(model_49)