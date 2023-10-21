import machine
import ssd1306py.ssd1306 as ssd1306
import math

_oled = None
_i2c = None
_width = 0
_height = 0


def init_i2c(scl, sda, width, height, i2c=1):
    """
    初始化i2c接口
    :param scl: i2c的时钟脚
    :param sda: i2c的数据脚
    :param width: oled屏幕的宽度像素
    :param height: oled屏幕的高度像素
    :param i2c: i2c口
    """
    global _oled, _width, _height
    _i2c = machine.I2C(i2c, scl=machine.Pin(scl), sda=machine.Pin(sda))
    _width = width
    _height = height
    _oled = ssd1306.SSD1306_I2C(_width, _height, _i2c)


def clear():
    """清除屏幕"""
    global _oled
    _oled.fill(0)


def show():
    """屏幕刷新显示"""
    global _oled
    _oled.show()


def pixel(x, y,value=1):
    """画点"""
    global _oled
    _oled.pixel(x, y, value)


def text(string, x_axis, y_axis):
    """显示字符串.注意字符串必须是英文或者数字"""
    global _oled
    _oled.text(string, x_axis, y_axis)
    return

def line_se(x_start,y_start,x_end,y_end):
    """画直线"""
    #垂直于x
    if x_start == x_end and y_start <= y_end:
        for i in range(y_start,y_end):
            pixel(x_start,i)
    elif x_start == x_end and y_start > y_end:
        for i in range(y_end,y_start):
            pixel(x_start,i)
    #垂直于y
    elif y_start == y_end and x_start <= x_end:
        for i in range(x_start,x_end):
            pixel(i,y_start)
    elif y_start == y_end and x_start > x_end:
        for i in range(x_end,x_start):
            pixel(i,y_start)
    elif x_end > x_start:
        dx = x_end - x_start
        dy = y_end - y_start
        k = dy / dx
        for x in range(x_start,x_end):
            y = round(k*x + x_start)
            pixel(x,y)
    elif x_end < x_start:
        x_start,x_end = x_end,x_start
        y_start,y_end = y_end,y_start
        dx = x_end - x_start
        dy = y_end - y_start
        k = dy / dx
        for x in range(x_start,x_end):
            y = round(k*x + x_start)
            pixel(x,y)
    else:
        pass
def matrix_2(lists,x_length,x=1,y=1):
    #二进制
    nx = int(1)
    ny = int(1)
    for i in lists:
        pixel(x+nx,y+ny,int(i))
        nx += 1
        if nx > int(x_length):
            nx = int(1)
            ny += 1
def tobin(value,length=8):
    v = str(bin(eval(value)))[2:]
    while len(v) < length:
        v = "0" + v
    return(v)
def matrix(lists,length,x=1,y=1):
    #画字符
    m = ""
    for i in lists:
        m += str(tobin(i,8))
        print(m)
    matrix_2(m,length,x,y)
def rounds(r,x,y,x_flex,y_flex):
    #画圆
    for i in range(0,6.29*100):
        nx = above(int(x) + eval(x_flex) * eval(r) * math.cos(i/100))
        ny = above(int(y) + eval(y_flex) * eval(r) * math.sin(i/100))
        pixel(nx,ny)
def square(x,y,x_length,y_length):
    #画矩形
    for i in range(0,int(x_length)):
        for n in range(0,int(ylength)):
            pixel(int(x) + i,int(y) + n)