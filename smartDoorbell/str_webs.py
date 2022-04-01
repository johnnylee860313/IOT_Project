from cmath import log
from copy import error
import os
import glob
import shutil
import datetime
import requests

import pandas as pd
import streamlit as st

from tqdm import tqdm
from PIL import Image

def rander_page():
    st.header('2022_NTU_IoT')
    st.title('Smar DoorBell(Lock)')
    usr = st.sidebar.text_input('用戶名', value='User_name')
    password = st.sidebar.text_input('密碼', value='password', type="password")
    mode = log_in(usr, password)
    if mode:
        st.success(f'Welcome {usr}!')
        rander_success()
    else:
        if usr == 'User_name':
            st.warning('請點選側邊欄輸入賬號密碼')
        else:
            st.error(f'Error {usr}!')

def rander_success():
    for i in os.listdir('./log'):
        df = pd.read_csv(os.path.join('./log', i))
        st.write(f'用戶{i.replace(".csv", "")}設備日誌')
        st.table(df)
        st.write('查看訪問日誌')
        left_column, right_column = st.columns(2)
        day = left_column.date_input("選擇日期", datetime.date(2022, 1, 1))
        time = right_column.time_input('選擇時間', datetime.time(8, 45))
        imgs, start_time, end_time = search_img(day, time)
        st.success(f'時間{start_time} ~ {end_time}內共存在失敗訪問請求共{len(imgs)}次!')
        if len(imgs) != 0:
            for img in imgs:
                image = Image.open(img)
                st.image(image, caption=img)
    return

def add_time(day, times, add):
    b = pd.to_datetime(str(day) + ' ' + str(times))   #类型为Timestamp

    if (b.minute + add) > 59:     ##超出60分钟界限，小时加1
        b = b.replace(hour = b.hour + 1)
        b = b.replace(minute = (b.minute + add) % 60)
    else:
        b = b.replace(minute = b.minute + add)
    return b

def search_img(day, times):

    start_time = add_time(day, times, -15)
    end_time = add_time(day, times, 15)
    imgs = []
    for img in os.listdir('./error_img'):
        img_time = img.replace('.jpg', '')
        img_time = datetime.datetime.strptime(img_time, "%Y-%m-%d %H:%M:%S")
        if start_time < img_time < end_time:
            print(img)
            imgs.append(os.path.join('./error_img', img))
    return imgs, start_time, end_time

def log_in(usr, password):
    df = pd.read_csv('./usrs.csv')
    if df[df.usr == usr].iloc[0, -1] == password:
        return True
    else:
        return False



if __name__ == '__main__':

    rander_page()


