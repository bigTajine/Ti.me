#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: Time.py
# Author: BigTajine
# Date created: 31/08/2022
# Date last modified: 08/09/2022
# Python version: 3.10.6

# Imports

"""
This is the source code of Ti.me; inspired by Time.is.
Ti.me uses the public IP address of your device and uses
IP Geolocation API to figure out your location based on IP.
"""

from tkinter import *
from ctypes import windll
import json
import requests
import sys
import time
import urllib.request

# Fixes blurry text encountered when using display scalling.

windll.shcore.SetProcessDpiAwareness(1)

# Initialization.

app = Tk()
app.title('Ti.me')
app.geometry('500x250')
app.iconbitmap('time.ico')
app.resizable(False, False)
app.configure(bg='#BFB9FA')
app.attributes('-topmost', True, '-alpha', 0.95)


def custom_label(
    parent,
    row,
    column,
    standard1,
    bold,
    standard2,
    ):

    cLabelFrame = Frame(parent, bg='#BFB9FA')
    cLabelFrame.grid(row=row, column=column)

    Label(cLabelFrame, text=standard1, font=('Lato', 12), fg='#333333',
          bg='#BFB9FA').grid(row=0, column=0)

    Label(cLabelFrame, text=bold, font=('Lato', 12, 'bold'),
          fg='#333333', bg='#BFB9FA').grid(row=0, column=1)

    Label(cLabelFrame, text=standard2, font=('Lato', 12), fg='#333333',
          bg='#BFB9FA').grid(row=0, column=2)


def get_date():
    current_date = time.strftime('%a, %d %b %Y')
    date_label.config(text=current_date)
    date_label.after(200, get_date)


def get_labels():
    frame = Frame(app, bg='#BFB9FA')

    try:
        custom_label(
            frame,
            0,
            0,
            'Time in ',
            dec_ip['city'] + ', ',
            dec_ip['countryCode'] + ' now',
            )
    except NameError:

        Label(frame, text='Time now', font=('Lato', 12), fg='#333333',
              bg='#BFB9FA').grid(row=0, column=0)
    global time_label
    time_label = Label(frame, font=('Montserrat', 36, 'bold'),
                       fg='#333333', bg='#BFB9FA')
    time_label.grid(row=1, column=0)
    global date_label
    date_label = Label(frame, font=('Lato', 12), fg='#333333',
                       bg='#BFB9FA')
    date_label.grid(row=2, column=0)

    # text = Text(frame, height=1, font="Lato 12")
    # text.tag_configure("bold", font="Lato 12 bold")
    # text.insert("end", "Time in ")
    # text.insert("end", dec_ip["city"], "bold")
    # text.insert("end", ", "+dec_ip["country"]+" now")
    # text.configure(state="disabled")
    # text.grid(row=3, column=0)

    frame.pack(expand=True)


def get_location():
    try:
        ip_api = 'http://ip-api.com/json/'
        request_ip = urllib.request.Request(ip_api)
        ip = urllib.request.urlopen(request_ip).read()
        global dec_ip
        dec_ip = json.loads(ip.decode('utf-8'))
    except urllib.error.URLError:
        None


def get_time():
    time_now = time.strftime('%H:%M:%S')
    time_label.config(text=time_now)
    time_label.after(200, get_time)


# Calling the functions below to allow for more order and oversight.

get_location()
get_labels()
get_time()
get_date()

app.mainloop()
