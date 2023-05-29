import threading
import time
import cv2
import RPi.GPIO as GPIO
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

PWMA = 18
AIN1 = 22
AIN2 = 27
PWMB = 23
BIN1 = 25
BIN2 = 24

def motor_back(speed):
     L_Motor.ChangeDutyCycle(speed)
     GPIO.output(AIN2,False) #AIN2
     GPIO.output(AIN1,True)  #AIN1
     R_Motor.ChangeDutyCycle(speed)
     GPIO.output(BIN2,False) #BIN2
     GPIO.output(BIN1,True)  #BIN1

def motor_go(speed):
     L_Motor.ChangeDutyCycle(speed)
     GPIO.output(AIN2,True)  #AIN2
     GPIO.output(AIN1,False) #AIN1
     R_Motor.ChangeDutyCycle(speed)
     GPIO.output(BIN2,True)  #BIN2
     GPIO.output(BIN1,False) #BIN1

def motor_stop():
     L_Motor.ChangeDutyCycle(0)
     GPIO.output(AIN2,False) #AIN2
     GPIO.output(AIN1,False) #AIN1
     R_Motor.ChangeDutyCycle(0)
     GPIO.output(BIN2,False) #BIN2
     GPIO.output(BIN1,False) #BIN1

def motor_right_45(left_speed, right_speed):
     L_Motor.ChangeDutyCycle(left_speed)
     GPIO.output(AIN2,True)  #AIN2
     GPIO.output(AIN1,False) #AIN1
     R_Motor.ChangeDutyCycle(right_speed)
     GPIO.output(BIN2,True) #BIN2
     GPIO.output(BIN1,False)  #BIN1

def motor_right_90(speed):
     L_Motor.ChangeDutyCycle(speed)
     GPIO.output(AIN2,True)  #AIN2
     GPIO.output(AIN1,False) #AIN1
     R_Motor.ChangeDutyCycle(0)
     GPIO.output(BIN2,True) #BIN2
     GPIO.output(BIN1,False)  #BIN1
     
def motor_right_super(left_speed, right_speed):
     L_Motor.ChangeDutyCycle(left_speed)
     GPIO.output(AIN2,True)  #AIN2
     GPIO.output(AIN1,False) #AIN1
     R_Motor.ChangeDutyCycle(right_speed)
     GPIO.output(BIN2,False) #BIN2
     GPIO.output(BIN1,True)  #BIN1

def motor_left_45(left_speed, right_speed):
     L_Motor.ChangeDutyCycle(left_speed)
     GPIO.output(AIN2,True)  #AIN2
     GPIO.output(AIN1,False) #AIN1
     R_Motor.ChangeDutyCycle(right_speed)
     GPIO.output(BIN2,True) #BIN2
     GPIO.output(BIN1,False)  #BIN1
     
def motor_left_90(speed):
     L_Motor.ChangeDutyCycle(0)
     GPIO.output(AIN2,False) #AIN2
     GPIO.output(AIN1,True)  #AIN1
     R_Motor.ChangeDutyCycle(speed)
     GPIO.output(BIN2,True)  #BIN2
     GPIO.output(BIN1,False) #BIN1
     
def motor_left_super(left_speed, right_speed):
     L_Motor.ChangeDutyCycle(left_speed)
     GPIO.output(AIN2,False)  #AIN2
     GPIO.output(AIN1,True) #AIN1
     R_Motor.ChangeDutyCycle(right_speed)
     GPIO.output(BIN2,True) #BIN2
     GPIO.output(BIN1,False)  #BIN1


GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(AIN2,GPIO.OUT)
GPIO.setup(AIN1,GPIO.OUT)
GPIO.setup(PWMA,GPIO.OUT)

GPIO.setup(BIN1,GPIO.OUT)
GPIO.setup(BIN2,GPIO.OUT)
GPIO.setup(PWMB,GPIO.OUT)

L_Motor= GPIO.PWM(PWMA,100)
L_Motor.start(0)

R_Motor = GPIO.PWM(PWMB,100)
R_Motor.start(0)

speedSet60 = 15
speedSet30 = 30
speedSet45 = 20
straightSpeedSet = 50
powerSpeedSet = 80


def img_preprocess(image):
     height, _, _ = image.shape
     image = image[int(height/2):,:,:]
     image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
     image = cv2.resize(image, (200,66))
     image = cv2.resize(image, (128,128))
     cv2.imshow('pre', image)

    #  image = cv2.GaussianBlur(image,(5,5),0)
    #  _,image = cv2.threshold(image,160,255,cv2.THRESH_BINARY_INV)
     image = image / 255
     return image
 
def show_test_img(image):
    height, _, _ = image.shape
    image = image[int(height/4):,:,:]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.resize(image, (300,300))
    cv2.imshow('pre', image)
#  image = cv2.GaussianBlur(image,(5,5),0)
#  _,image = cv2.threshold(image,160,255,cv2.THRESH_BINARY_INV)

 

camera = cv2.VideoCapture(-1)
camera.set(3, 640)
camera.set(4, 480)


def main():
    model_path = "/home/donguk/AI_CAR/model/class5_20_epochs.h5"
    model = load_model(model_path)
    carState = 'stop'
    try:
        while True:
            keyValue = cv2.waitKey(1)
            if keyValue == ord('q'):
                break
            elif keyValue == 82:
                print("go")
                carState = "go"
            elif keyValue == 84:
                print("stop")
                carState = 'stop'
                
            _ ,image = camera.read()
            image = cv2.flip(image,-1)
            preprocessed = img_preprocess(image)
            
            show_test_img(image)
            
            #cv2.imshow('pre', preprocessed)
            X = np.asarray([preprocessed])
            # steering_angle = int(model.predict(X)[0])
            # print("predict angle:",steering_angle)
            
            predictions = model.predict(X)
            
            # get max prediction index probability
            # max prediction index
            max_probability_index = np.argmax(predictions, axis=1)
            print("predicted class indices:", max_probability_index)
            steering_angle = max_probability_index 
            
            predictions = np.round(predictions[0], 3)#[round(pred, 3) for pred in predictions[0]]
            sorted_predictions = sorted(enumerate(predictions), key=lambda x: x[1], reverse=True)
            print(sorted_predictions)
            
            if carState == "go":
                if steering_angle == 0:
                    print("left90")
                    motor_left_90(straightSpeedSet)
                elif steering_angle == 1:
                    print("left45")
                    motor_left_45(speedSet45, straightSpeedSet)
                elif steering_angle == 2 :
                    print("go")
                    motor_go(straightSpeedSet)
                elif steering_angle == 3:
                    print("right45")
                    motor_right_45(straightSpeedSet, speedSet45)
                elif steering_angle == 4 :
                    print("right90")
                    motor_left_90(straightSpeedSet)          
                elif carState == "stop":
                    motor_stop()

        #label_list =[0, 30, 60, 90, 120, 150, 180]

    except KeyboardInterrupt:
          pass
if __name__ == '__main__':
     main()
     cv2.destroyAllWindows()
            
