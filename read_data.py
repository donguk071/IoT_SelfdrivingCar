import glob
from PIL import Image
import numpy as np
import random
from sklearn.model_selection import train_test_split
import re
import tensorflow as tf
import matplotlib.pyplot as plt

#label_list =[0, 30, 60, 90, 120, 150, 180, -30, 210]
label_list =[0, 45, 90, 135, 180]

def get_label_from_filename(filename):
    cvurrnet_label = re.findall(r'\d+', filename)[-1]  # 파일명에서 숫자 부분 추출
    for i,label in enumerate(label_list):
        if label == int(cvurrnet_label):
            return int(i)
        # else:
        #     print("dont have label", int(cvurrnet_label))
    return int(100)

class DataReader:
    def __init__(self):
        self.x_train = []
        self.x_test = []
        self.y_train = []
        self.y_test = []
        
        self.target = []
        
    def f_data_reader(self, img_size = (0,0), batch_size = 32):
        file_path = []
        folder = glob.glob('data/*')
        for f in folder:
            file_path += glob.glob(str(f) + "/*")

        print("len files : " , len(file_path))
        
        data = []
        for i, path in enumerate(file_path):
            img = Image.open(path)
            if img_size[0] != 0 :
                img_ref = img.resize((img_size[0], img_size[1]))
                
            img = np.asarray(img_ref)
            label = get_label_from_filename(path)
            data.append((img, label))
            img_ref.close()
            if i % 5000 == 0:
                print("processed : {} / {}".format(i,len(file_path)) )
       
         
        random.shuffle(data)

        target = [row[1] for row in data]
        self.target = target
        data = [row[0] for row in data]
        num_label = len(np.unique(target))
        print(np.unique(target))
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

        # target 리스트에 저장된 값들의 분포 그래프 그리기
        plt.hist(target)
        plt.title("Distribution of Target Values")
        plt.xlabel("Target Values")
        plt.ylabel("Frequency")
        plt.show()
        
# test = DataReader()
# test.f_data_reader(200)
# plt.hist(test.target)
# plt.title("Distribution of Target Values")
# plt.xlabel("Target Values")
# plt.ylabel("Frequency")
# plt.show()
