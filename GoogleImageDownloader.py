#!/usr/bin/env python3


import tkinter as tk
import tkinter.messagebox as tkm
import tkinter.ttk as ttk
import subprocess
import json
import requests
import urllib.request
import os

ke=None
cse=None
parent_folder=None
try:
    fs=open("set.config","r")
    string=fs.read()
    lst=json.loads(string)
    ke=lst[0]
    cse=lst[1]
    parent_folder=lst[2]
except:
    pass

def setconfig():
    global ke,cse,parent_folder,win,canvas
    win=tk.Tk()
    win.title("Config Settings")
    canvas= tk.Canvas(win,height=400,width=400,bg="black",highlightbackground="black",highlightthickness=0)
    canvas.pack()
    par_frame=tk.Frame(canvas,bd=0,bg="black",highlightbackground="black",highlightthickness=0)
    par_frame.pack()
    f3=tk.Frame(par_frame,bd=0,bg="black",highlightbackground="black",highlightthickness=0)
    f3.pack(side="left")
    f4=tk.Frame(par_frame,bd=0,bg="black",highlightbackground="black",highlightthickness=0,pady=2)
    f4.pack(side="right")

    L3=tk.Label(f3, text="Key               ",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
    L3.pack()
    global e3
    e3=tk.Entry(f4,fg="white",bg="black")
    if ke!=None:
        e3.insert(0,ke)
    e3.pack()

    L4=tk.Label(f3, text="CSE ID           ",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
    L4.pack()

    global e4
    e4=tk.Entry(f4,fg="white",bg="black")
    if cse!=None:
        e4.insert(0,cse)
    e4.pack()
    L5=tk.Label(f3, text="Parent Folder",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
    L5.pack()
    global e5
    e5=tk.Entry(f4,fg="white",bg="black")
    if parent_folder!=None:
        e5.insert(0,parent_folder)
    e5.pack()
    w3 = tk.Button(canvas,text="Save", command= saveconfig,fg="white",bg="black",activeforeground="white",activebackground="#323232",bd=0)
    w3.pack()

def saveconfig():
    global ke,cse,parent_folder,e3,e4,e5,win
    fst=open("/root/Python_codes/set.config","w")
    ke=e3.get()
    cse=e4.get()
    parent_folder=e5.get()
    lst=[ke,cse,parent_folder]
    fst.write(json.dumps(lst))
    fst.close()
    win.destroy()



def gotodir(name):
    global parent_folder
    if os.getcwd() != parent_folder:
        os.chdir(parent_folder)
    if os.getcwd() == parent_folder:
        if name not in os.listdir():
            os.mkdir(name)
        os.chdir(name)
def gimg_download():
    global ke,cse,parent_folder,e1,e2
    if cse==None or ke==None or parent_folder==None:
        print("error")
        return

    site="https://www.googleapis.com/customsearch/v1?"
    name=e1.get()
    num=e2.get()
    page=requests.get(site,params={"key":ke,"cx":cse,"q":name,"num":num,"start":"0","searchType":"image","imgSize":"huge"})
    diction=page.json()
    lst=[]
    if "items" not in diction:
        print("No results found!")
    else:
        ls=name.split()
        new_name="_".join(ls)
        gotodir(new_name)
        for di in diction["items"]:
            sty=di["fileFormat"]
            sr=sty[6:len(sty)]
            lst.append((di["link"],sr))
        i=0
        for link in lst:
            try:
                urllib.request.urlretrieve(link[0],new_name+"_"+str(i)+'.'+link[1])
                print("Downloaded "+ str(i+1)+" image(s)")
                i+=1
            except:
                print("There was some error")

    tkm.showinfo("Prompt","Done")


##########################################################
top= tk.Tk()
top.title("Google Image Downloader")
ic=tk.PhotoImage(file=r'download.gif')
# style = ThemedStyle(top)
# style.set_theme("black")

top.tk.call('wm', 'iconphoto', top._w, ic)
#####################################
#canvas
canva= tk.Canvas(top,height=400,width=400,bg="black",highlightbackground="black",highlightthickness=0)
canva.pack()
#######################################
## Top MenuBar

menuBar=tk.Menu(top,bg="black",fg="white")
top.config(menu=menuBar)
subMenu=tk.Menu(menuBar, tearoff=0,fg="white",bg="black")
menuBar.add_cascade(label="Settings",menu=subMenu,activeforeground="white",activebackground="#323232")
subMenu.add_command(label="Config Settings",command=setconfig,activeforeground="white",activebackground="#323232")

#######################################
file_n=tk.PhotoImage(file="downloadtree.png")
w = tk.Button(canva, image= file_n,bg="black",bd=0,highlightbackground="black",highlightthickness=0)
w.pack()
butn=tk.PhotoImage(file="search2.png")
pframe=tk.Frame(canva,bd=0,highlightbackground="black",highlightthickness=0)
pframe.pack()
f1=tk.Frame(pframe,bd=0,bg="black",highlightbackground="black",highlightthickness=0,pady=3)
f1.pack(side="left")
f2=tk.Frame(pframe,bd=0,bg="black",highlightbackground="black",highlightthickness=0)
f2.pack(side="right")

L1=tk.Label(f1, text="Search Text   ",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
L1.pack()#
e1=tk.Entry(f2,fg="white",bg="black")
e1.pack()#side="left"

L2=tk.Label(f1, text="Search Count ",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)#
L2.pack()#side="left"
e2=tk.Entry(f2,fg="white",bg="black")#
e2.pack()#side="right"
########################################################3
######################################################3##
w2 = tk.Button(canva, image=butn,command= gimg_download,fg="white",bg="black",activebackground="#323232",bd=0,highlightbackground="black",highlightthickness=0)#
w2.pack()
top.mainloop()
