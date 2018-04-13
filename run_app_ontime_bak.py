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
x_start=65000;
y_start=1000;
sleep1_time=2;
sleep2_time=2;
running_interval=5;
restart_interval=5;
loop_num=5;

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))


class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))


class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))


def MouseInput(flags, x, y, data):
    return MOUSEINPUT(x, y, data, flags, 0, None)


def KeybdInput(code, flags):
    return KEYBDINPUT(code, code, flags, 0, None)


def HardwareInput(message, parameter):
    return HARDWAREINPUT(message & 0xFFFFFFFF, parameter & 0xFFFF, parameter >> 16 & 0xFFFF)


INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARD = 2


def Input(structure):
    if isinstance(structure, MOUSEINPUT):
        return INPUT(INPUT_MOUSE, _INPUTunion(mi=structure))
    if isinstance(structure, KEYBDINPUT):
        return INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure))
    if isinstance(structure, HARDWAREINPUT):
        return INPUT(INPUT_HARDWARE, _INPUTunion(hi=structure))
    raise TypeError('Cannot create INPUT structure!')


def Mouse(flags, x=0, y=0, data=0):
    return Input(MouseInput(flags, x, y, data))


def Keyboard(code, flags=0):
    return Input(KeybdInput(code, flags))


def Hardware(message, parameter=0):
    return Input(HardwareInput(message, parameter))

def SendInput(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
    return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)

def start_app():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' start '+ app_name);
    os.chdir(app_dir);
    win32api.ShellExecute(0,'open',app_name,'','',1);
    m=PyMouse();
    # time.sleep(2);
    # hwnd=win32gui.FindWindow(0,u'振动数据采集与分析系统');
    # print(hwnd);
    time.sleep(2);
    # #win32gui.SetForegroundWindow(hwnd);
    # #win32api.SetCursorPos((x_test,y_test));
    # #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_LEFTUP,0,0,0,0);
    m.move(x_test,y_test);
    time.sleep(1);
    # #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_LEFTUP,0,0,0,0);
    m.click(x_test,y_test);
    # #m.click(x_test,y_test);
    # #time.sleep(sleep2_time);
    # # time.sleep(5);
    # m.move(x_start,y_start);
    # # time.sleep(1);
    # # m.click(x_start,y_start,1);
    # # m.click(x_start,y_start,1);
    # ctypes.windll.user32.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN+win32con.MOUSEEVENTF_LEFTUP,0,0,0,0);
    # #ctypes.windll.user32.SetCursorPos((x_start,y_start));
    # ctypes.windll.user32.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_LEFTUP|win32con.MOUSEEVENTF_ABSOLUTE
    # 					,x_start,y_start,0,0);
    # SendInput(Mouse(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, x_start,y_start));
    # SendInput(Mouse( win32con.MOUSEEVENTF_LEFTDOWN |win32con.MOUSEEVENTF_ABSOLUTE, x_start,y_start));
    # SendInput(Mouse( win32con.MOUSEEVENTF_LEFTUP |win32con.MOUSEEVENTF_ABSOLUTE, x_start,y_start));
    timer=threading.Timer(running_interval,kill_app);
    timer.start();

def kill_app():
    global loop_num;
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' kill '+app_name+ ' and restart it');
    os.chdir(app_dir);
    #os.system('TASKKILL /F /IM '+app_name);
    loop_num-=1;
    if(loop_num>5):
        timer=threading.Timer(restart_interval,start_app);
        timer.start();

#sdef

if __name__=='__main__':
    start_app();


