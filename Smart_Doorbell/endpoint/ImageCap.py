import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

name = 'Detection'

cam = PiCamera()
cam.resolution(512,304)
cam.framerate = 10
rawcapture = PiRGBArray(cam,size=(512,304))

img_counter = 0

while True:
    for frame in cam.capture_continuous(rawCapture,format="bgr",use_video_port=True):
        image = frame.array
        cv2.imshow("press dpace to take a photo")
        rawCapture.truncate(0)

        k = cv2.waitkey(1)
        rawCapture.truncate(0)
        if k%256 == 27:#esc pressed
            break
        elif k%256 == 32:#space pressed
            img_name = "Documents"+name+"/image_{}.jpg".format(img_counter)
            cv2.imwrite(img_name,image)
            print("{} wirtten!".format(img_name))
            img_counter += 1
    
    if k%256 == 27:
        print("Esc hit,closing ......")
        break

cv2.destroyAllWindows()
