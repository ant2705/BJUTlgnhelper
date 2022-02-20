import requests
from tkinter import *
import os
import hashlib
###only support windows
cpu = os.popen('wmic cpu get processorid').read()
cpumd5 = hashlib.md5(cpu.encode()).hexdigest()
key1 = ord(cpumd5[0])
key2 = ord(cpumd5[1])
key3 = ord(cpumd5[2])
key4 = ord(cpumd5[3])

window = Tk()
window.title = "v0.3"
infolabel = Label(window, text="请在下面输入用户名和密码。\nBy Ant\n")
infile = open("lgn.wc2s","a")
infile = open("lgn.wc2s","r")

def main():
    if(infile.read().find("autowc2s")!=-1):
        infolabel.pack()
        #print("autowc2s found!")
        autolgn()
    else:
        usernameentry = Entry(window)
        passentry = Entry(window, show= '*')
        lgnbutton = Button(window, text = "登录", command = lambda:lgnclicked(usernameentry.get(), passentry.get()) )
        infolabel.pack()
        usernameentry.pack()
        passentry.pack()
        lgnbutton.pack()
    window.mainloop()

def lgnclicked(username,passwd):
    infile = open("lgn.wc2s","w")
    infile.write("autowc2s\n")
    infile.write(username)
    infile.write("\n")
    for i in passwd:
        t = (ord(i)+key1)*key2 - key3 + key4
        infile.write(str(t))
        infile.write("\n")
    infile.write(str(0))
    aa = requests.get('http://lgn.bjut.edu.cn')
    if(aa.status_code == 200):
        if(logstatus() == 0):
            loginf(username,passwd)

def autolgn():
    infile = open("lgn.wc2s","r")
    infile.readline()
    username = infile.readline()
    username = username.replace("\n","")
    username = username.replace("\r","")
    #print("username:",username)
    passwd = ""
    while(1):
        t = eval(infile.readline())
        #print(t)
        if(t == 0):
            break
        passwd += chr((t+key3-key4)//key2 - key1)
    aa = requests.get('http://lgn.bjut.edu.cn')
    if(aa.status_code == 200):
        if(logstatus() == 0):
            loginf(username,passwd)
        elif(logstatus() == 1):
            infolabel.config(text= "您目前已经登录了网关。请注销后再重新打开该程序以完成配置。")
        else:
            infolabel.config(text= "网关状态未知。请检查网络连接，并从网关注销后再重新打开该程序以完成配置。")
    else:
        infolabel.config(text= "无法访问网关。请检查网络连接后再试。")

def logstatus():
    ss = requests.get("http://lgn.bjut.edu.cn/").text
    #print(ss)
    if(ss.find("<title>北京工业大学上网登录窗")!=-1):
        #未登录
        return 0
    elif(ss.find("<title>登录成功窗")!=-1):
        #登陆成功
        return 1
    elif(ss.find("<title>北京工业大学上网信息窗")):
        return 1
    return -1

def loginf(username,passwd):
    data2={'DDDDD':username,
           'upass':passwd,
           '0MKKey':'%B5%C7%C2%BC+Login'}

    back=requests.post("http://lgn.bjut.edu.cn/",data=data2,timeout=5).text
    #print(back)
    if(back.find("<title>登录成功窗")!=-1):
        infolabel.config(text= "登陆成功")
        #print("登陆成功")
        return 1
    return 0


main()
