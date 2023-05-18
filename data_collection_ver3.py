import cv2
import RPi.GPIO as GPIO
from datetime import datetime
import os

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

def motor_right_30(left_speed, right_speed):
     L_Motor.ChangeDutyCycle(left_speed)
     GPIO.output(AIN2,True)  #AIN2
     GPIO.output(AIN1,False) #AIN1
     R_Motor.ChangeDutyCycle(right_speed)
     GPIO.output(BIN2,True) #BIN2
     GPIO.output(BIN1,False)  #BIN1

def motor_right_60(left_speed, right_speed):
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

def motor_left_30(left_speed, right_speed):
     L_Motor.ChangeDutyCycle(left_speed)
     GPIO.output(AIN2,True)  #AIN2
     GPIO.output(AIN1,False) #AIN1
     R_Motor.ChangeDutyCycle(right_speed)
     GPIO.output(BIN2,True) #BIN2
     GPIO.output(BIN1,False)  #BIN1

def motor_left_60(left_speed, right_speed):
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
straightSpeedSet = 50
powerSpeedSet = 80


def main():
     camera = cv2.VideoCapture(-1)
     camera.set(3, 640)
     camera.set(4, 480)
     
     now = datetime.now()
     month = f"{now.month:02d}"
     day = f"{now.day:02d}"
     hour = f"{now.hour:02d}"
     minute = f"{now.minute:02d}"
     
     
     current_time = month + day + hour + minute
     filepath = f"/home/donguk/AI_CAR/video/train/{current_time}"
     os.makedirs(filepath, exist_ok=True)
     i = 0
     carState = "stop"

     while( camera.isOpened() ):
          keyValue = cv2.waitKey(10)
          if keyValue == ord("q"):
               break
          elif keyValue == ord("6"):
               print("go")
               carState = "go"
               motor_go(straightSpeedSet)
          elif keyValue == ord("g"):
               print("stop")
               carState = "stop"
               motor_stop()
          elif keyValue == ord("y"):
               print("right30")
               carState = "right30"
               motor_right_30(straightSpeedSet, speedSet30)
          elif keyValue == ord("u"):
               print("right60")
               carState = "right60"
               motor_right_60(straightSpeedSet, speedSet60)
          elif keyValue == ord("j"):
               print("right90")
               carState = "right90"
               motor_right_90(straightSpeedSet)
          elif keyValue == ord("k"):
               print("right90_power")
               carState = "right90_power"
               motor_right_90(powerSpeedSet)
          elif keyValue == ord("l"):
               print("right_super")
               carState = "right_super"
               motor_right_super(straightSpeedSet, speedSet30)
          elif keyValue == ord("a"):
               print("left_super")
               carState = "left_super"
               motor_left_super(speedSet60, straightSpeedSet)
          elif keyValue == ord("t"):
               print("left30")
               carState = "left30"
               motor_left_30(speedSet30, straightSpeedSet)
          elif keyValue == ord("r"):
               print("left60")
               carState = "left60"
               motor_left_60(speedSet60, straightSpeedSet)
          elif keyValue == ord("d"):
               print("left90")
               carState = "left90"
               motor_left_90(straightSpeedSet)
          elif keyValue == ord("s"):
               print("left90_power")
               carState = "left90_power"
               motor_left_90(powerSpeedSet)
          elif keyValue == ord("a"):
               print("left_super")
               carState = "left_super"
               motor_left_super(speedSet30, straightSpeedSet)

          _, image = camera.read()
          image = cv2.flip(image,-1)
          cv2.imshow('Original', image)
          height, _, _ = image.shape 
          save_image = image[int(height/2):,:,:]
          save_image = cv2.cvtColor(save_image, cv2.COLOR_BGR2YUV)
          save_image = cv2.GaussianBlur(save_image, (3,3), 0)
          save_image = cv2.resize(save_image, (200,66))
          cv2.imshow('Save', save_image)
          
          if carState == "left90":
               cv2.imwrite(f"{filepath}/train_{current_time}_{i:05d}_000.png", save_image)
               i += 1
          elif carState == "left60":
               cv2.imwrite(f"{filepath}/train_{current_time}_{i:05d}_030.png", save_image)
               i += 1
          elif carState == "left30":
               cv2.imwrite(f"{filepath}/train_{current_time}_{i:05d}_060.png", save_image)
               i += 1
          elif carState == "go":
               cv2.imwrite(f"{filepath}/train_{current_time}_{i:05d}_090.png", save_image)
               i += 1
          elif carState == "right30":
               cv2.imwrite(f"{filepath}/train_{current_time}_{i:05d}_120.png", save_image)
               i += 1
          elif carState == "right60":
               cv2.imwrite(f"{filepath}/train_{current_time}_{i:05d}_150.png", save_image)
               i += 1
          elif carState == "right90":
               cv2.imwrite(f"{filepath}/train_{current_time}_{i:05d}_180.png", save_image)
               i += 1

     cv2.destroyAllWindows()

if __name__ == "__main__":
     main()
     GPIO.cleanup()

