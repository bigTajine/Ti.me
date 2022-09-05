#!/usr/env python

# File name: Time.py
# Author: BigTajine
# Date created: 31/08/2022
# Date last modified: 05/09/2022
# Python version: 3.10.6

"""
This is the source code of Ti.me; inspired by Time.is.
Ti.me uses the public IP address of your device and uses
IP Geolocation API to figure out your location based on IP.
"""

# Imports
from tkinter import *
from ctypes import windll
import json
import requests
import sys
import time
import urllib.request

# Fixes blurry text encountered when using display scalling.
windll.shcore.SetProcessDpiAwareness(1)

app = Tk()
app.title("Ti.me")
app.geometry("500x250")
app.iconbitmap("time.ico")
app.resizable(False, False)
app.configure(bg = "#BFB9FA")
app.attributes('-topmost', True)

"""
Here below I created all the functions needed for Ti.me.
Put them in alphabetical order to make everything more organized.
"""

def get_date():
    current_date = time.strftime("%a, %d %b %Y")
    date_label.config(text = current_date)
    date_label.after(200, get_date)

def get_labels():
    frame = Frame(app, bg='#BFB9FA')
    Label(frame, text = ("Time in " + json_response["city"] + ", " + json_response["country"] + " now"), font = ("Lato", 12), fg = "#333333", bg = "#BFB9FA").grid(row=0, column=0)
    global time_label
    time_label = Label(frame, font = ("Montserrat", 36, "bold"), fg = "#333333", bg = "#BFB9FA")
    time_label.grid(row=1, column=0)
    global date_label
    date_label = Label(frame, font = ("Lato", 12), fg = "#333333", bg = "#BFB9FA")
    date_label.grid(row=2, column=0)
    frame.pack(expand=True) 

def get_location():
    geo_ip_api_url = "http://ip-api.com/json/"
    req = urllib.request.Request(geo_ip_api_url)
    response = urllib.request.urlopen(req).read()
    global json_response
    json_response = json.loads(response.decode("utf-8"))

def get_time():
    current_time = time.strftime("%H:%M:%S")
    time_label.config(text = current_time)
    time_label.after(200, get_time)

# Calling the functions below to allow for more order and oversight.
get_location()
get_labels()
get_time()
get_date()

app.mainloop()