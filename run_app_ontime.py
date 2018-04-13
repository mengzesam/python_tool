# -*- coding:utf-8 -*-
import time;
import  threading;
import os;
import win32api;
import win32con;
import win32gui;
import ctypes
from pymouse import  PyMouse;

app_name='ECAEVM.exe';
app_dir=r'd:\work\2018.4.11vib';
x_test=1180;
y_test=40;
x_start=500;
y_start=150;
sleep1_time=5;
sleep2_time=1;
running_interval=5;
restart_interval=5;
loop_num=5;

def start_app():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' start '+ app_name);
    os.chdir(app_dir);
    win32api.ShellExecute(0,'open',app_name,'','',1);
    m=PyMouse();
    time.sleep(sleep1_time);
    m.move(x_test,y_test);
    time.sleep(sleep2_time);
    m.click(x_test,y_test);
    m.move(x_start,y_start);
    time.sleep(sleep2_time);
    m.click(x_start,y_start);
    timer=threading.Timer(running_interval,kill_app);
    timer.start();

def kill_app():
    global loop_num;
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' kill '+app_name+ ' and restart it');
    os.chdir(app_dir);
    os.system('TASKKILL /F /IM '+app_name);
    loop_num-=1;
    if(loop_num>0):
        timer=threading.Timer(restart_interval,start_app);
        timer.start();


if __name__=='__main__':
    start_app();


