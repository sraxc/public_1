import subprocess
import time

def GetDriverList(detail=1):
    cmd = "hdc list targets"
    if detail == 1 or detail == True:
        cmd = cmd + " -v"
    returnall = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, encoding="gbk"
    ).stdout
    returnlist = returnall.split("\n")[1:]
    returnlists = []
    for i in returnlist:
        if str(i) != "":
            # newlist = i.split()
            returnlists.append(i)
    return returnlists


def installhap(driverName, hapPath, separator="/"):
    # separator 路径分隔符
    hapname = str(hapPath).split(separator)[-1]
    subprocess.run("hdc -t {} file send {} /sdcard/ed086ac90ae94a6b32b0c44526049e5e/{}".format(driverName, hapPath, hapname),shell=True,stdout=subprocess.PIPE,encoding="gbk",).stdout
    a = subprocess.run("hdc -t {} shell bm install -p /sdcard/ed086ac90ae94a6b32b0c44526049e5e/".format(driverName),shell=True,stdout=subprocess.PIPE,encoding="gbk",).stdout
    subprocess.run("hdc -t {} shell rm -rf /sdcard/ed086ac90ae94a6b32b0c44526049e5e".format(driverName),shell=True,stdout=subprocess.PIPE,encoding="gbk",).stdout
    return a

def GetAPI(driverName):
    a = subprocess.run(
        "hdc -t {} shell getprop hw_sc.build.os.apiversion".format(driverName),
        shell=True,
        stdout=subprocess.PIPE,
        encoding="gbk",
    ).stdout
    return a


###########################################################GUI##################################################
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

####   chosedriver  已选择设备


def refreshlist():
    listbox1.delete(0, tk.END)
    global driverlist  # 设备列表
    driverlist = GetDriverList()
    if len(driverlist) != 0:
        for i in driverlist:
            listbox1.insert(tk.END, i)
    else:
        listbox1.insert(tk.END, "（无设备）")


def callback1():
    try:
        value = str(listbox1.curselection())[1]
        global chosedriver
        chosedriver = str(str(driverlist[int(value)]).split()[0])
        txt.set(chosedriver)
    except:
        warnbox("error", "未选择设备")


def messageboxs(titles, messages):
    messagebox.showinfo(title=titles, message=messages)


def warnbox(titles, messages):
    messagebox.showerror(title=titles, message=messages)


def callback2():
    try:
        api = str(GetAPI(chosedriver))
        messageboxs("API", api)
    except:
        warnbox("error", "未选择设备")


def select_file():
    # 单个文件选择
    global selected_file_path
    selected_file_path = filedialog.askopenfilename()  # 使用askopenfilename函数选择单个文件
    select_path.set(selected_file_path)


def bu_install():
    try:
        a = installhap(chosedriver, selected_file_path)
        messageboxs(titles="",messages=a)
    except:
        warnbox("error", "未选择设备或未选择文件")


win = tk.Tk()
win.geometry("410x280")
win.title("hdc GUI v0.1.0")

###左栏###
listbox1 = tk.Listbox(
    win, width=20, height=10, xscrollcommand=True, yscrollcommand=True
)
listbox1.place(x=10, y=10)
refreshlist()
tk.Button(win, text="确定", command=callback1).place(x=10, y=200, width=70, height=30)
tk.Button(win, text="刷新", command=refreshlist).place(x=80, y=200, width=70, height=30)
txt = tk.StringVar()
tk.Entry(win, textvariable=txt).place(x=10, y=240, width=150, height=30)


###右栏###
tk.Button(win, text="查询API", command=callback2).place(x=180, y=10, width=180, height=30)

select_path = tk.StringVar()

tk.Entry(win, textvariable=select_path).place(x=180, y=60, width=140, height=30)
tk.Button(win, text="选择.hap文件", command=select_file).place(x=320, y=60, width=80, height=30)
tk.Button(win, text="安装.hap软件", command=bu_install).place(x=180, y=110, width=180, height=30)

win.mainloop()
