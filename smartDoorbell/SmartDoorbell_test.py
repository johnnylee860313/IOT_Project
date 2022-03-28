import RPi.GPIO as GPIO
import time
import os
import json
import base64
import requests
from PIL import Image
import numpy as np
import urllib.request
from picamera import PiCamera
from json import encoder


# face recongnition task
def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=HLeB6tlQqrnzZO6le9m2qz8T&client_secret=VaOCT9NvEkW9vxYfudDmWFaGu48B8fxQ'
    response = requests.get(host)
    access_token = response.json()['access_token']
    return access_token

def get_match(input_img):
    # input: 捕捉到的的現場圖片路徑
    access_token = get_token()
    _codes, scores = [], []
    # TODO usr  face dir
    usrs = os.listdir('./usr')
    for usr in usrs:
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
        f = open(os.path.join('./usr', usr), 'rb')
        f2 = open(input_img, 'rb')
        # img to base64
        raw_face = str(base64.b64encode(f.read()), 'utf-8')
        input_face = str(base64.b64encode(f2.read()), 'utf-8')
        params = [{'image': raw_face,
                    'image_type': 'BASE64',
                    'face_type': 'LIVE',
                    'quality_control': 'LOW',
                    'liveness_control': 'NORMAL'
                },
                {'image': input_face,
                    'image_type': 'BASE64',
                    'face_type': 'LIVE',
                    'quality_control': 'LOW',
                    'liveness_control': 'NORMAL'
                }]
        params = json.dumps(params, ensure_ascii=False)
        params = json.loads(params)
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, json=params, headers=headers)
        if response:
            response = response.json()
            _code = response['error_code']
            _codes.append(_code)
            if _code != 0:
                continue
            res = response['result']
            scores.append(res['score'])
    # remove __cache__/img
    if scores == []:
        print(_codes)
        return 'API ERROR', str(_codes)
    match_res = np.argsort(np.array(scores))
    if scores[match_res[-1]] >= 75.0:
        return 'Success', usrs[match_res[0]].split('.')[0]
    else:
        return 'No Match', -1

#raspi task

BUTTON_PIN = 25
LED_PIN = 17
LOCK_GPIO = 23
PWM_FREQ = 50
STEP=15
degrees = [45, 90, 135, 90]
count = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(LOCK_GPIO, GPIO.OUT)
GPIO.setup(BUTTON_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN,GPIO.OUT)

pwm = GPIO.PWM(LOCK_GPIO, PWM_FREQ)
pwm.start(0)

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle

def switch2deg(deg):
    dc = angle_to_duty_cycle(deg)
    pwm.ChangeDutyCycle(dc)

def post_img(path, mode = 'Error'):
    img = Image.open(os.path.join('./__cache__/', path))
    w, h =img.size
    img_resize = img.resize((int(w*0.5), int(h*0.5)))
    img_resize.save(os.path.join('./__cache__/', path))

    f = open(os.path.join('./__cache__/', path), 'rb')
    encoder = str(base64.b64encode(f.read()), 'utf-8')

    msg1 = {'image': encoder,
              'mode': mode,
            }
    jmsg1 = json.dumps(msg1)
    print(jmsg1)
    urllib.request.urlopen(f'http://140.112.18.2:11064/{str(jmsg1).replace(" ","%20")}')


while True:
    BUTTON_STATUS = GPIO.input(BUTTON_PIN)
    if(BUTTON_STATUS == True):
        print("Button unpressed")
        GPIO.output(LED_PIN,0)
    else:
        print("Button pressed")
        GPIO.output(LED_PIN,1)
        # Photo
        camera = PiCamera()
        camera.resolution = (640,480)
        camera.vflip = True
        camera.start_preview()
        time.sleep(1)
        camera.capture('./__cache__/'+str(count)+'.jpg')
        camera.close()
        # save to ./__cache__/xxx.jpg
        msg, usr_token = get_match('./__cache__/'+str(count)+'.jpg')
        if msg == 'No Match':
            # 140.140.140.140/2022-03-07-14:30-usr_token-open
            # open the door
            print("Door opened")
            for i in range(5):
                for deg in degrees:
                    switch2deg(deg)
                    time.sleep(0.5)
            pwm.stop()
            GPIO.cleanup()
            post_img(str(count)+'.jpg', mode='success')
        elif msg == 'API ERROR':
            print('ERROR try again')
            os.remove('./__cache__/'+str(count)+'.jpg')
        elif msg == 'Success':
            # post WEB
            # save to dir
            os.rename('./__cache__/'+str(count)+'.jpg','./guest_history/'+str(count)+'.jpg')
            print("Stranger without register.")
            post_img(str(count)+'.jpg')
    count=count+1
    time.sleep(0.5)
