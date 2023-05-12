import glob
from PIL import Image
import numpy as np
import random
from sklearn.model_selection import train_test_split
import re
import tensorflow as tf

label_list =[0, 30, 60, 90, 120, 150, 180]

def get_label_from_filename(filename):
    cvurrnet_label = re.findall(r'\d+', filename)[-1]  # 파일명에서 숫자 부분 추출
    for i,label in enumerate(label_list):
        if label == int(cvurrnet_label):
            return int(i)
    return int(100)

class DataReader:
    def __init__(self):
        self.x_train = []
        self.x_test = []
        self.y_train = []
        self.y_test = []
    def f_data_reader(self, img_size = 0):
        file_path = []
        folder = glob.glob('data/*')
        for f in folder:
            file_path += glob.glob(str(f) + "/*")

        print("len files : " , len(file_path))
        
        data = []
        for i, path in enumerate(file_path):
            img = Image.open(path)
            if img_size != 0 :
                img = img.resize((img_size, img_size))
            img = np.asarray(img)
            label = get_label_from_filename(path)
            data.append((img, label))
         
        random.shuffle(data)

        target = [row[1] for row in data]
        data = [row[0] for row in data]
        num_label = len(np.unique(target))
        print("num class : ", num_label)
        #one hot
        #stf.keras.utils.to_categorical(target, num_label)
        
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
        data, target, test_size=0.2, shuffle=True, stratify=target, random_state=34)
        self.x_train = np.array(self.x_train) / 255.0
        self.x_test = np.array(self.x_test) / 255.0
        self.y_train = np.array(self.y_train) / 1.0
        self.y_test = np.array(self.y_test) / 1.0

        print("\n\nData Read Done!")
        print("Training X Size : " + str(self.x_train.shape))
        print("Training Y Size : " + str(self.y_train.shape))
        print("Test X Size : " + str(self.x_test.shape))
        print("Test Y Size : " + str(self.y_test.shape) + '\n\n')