#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: Time.py
# Author: BigTajine
# Date created: 31/08/2022
# Date last modified: 18/09/2022
# Python version: 3.10.7

"""
This is the source code of Ti.me; inspired by Time.is.
Ti.me uses the public IP address of your device and uses
an IP Geolocation API to figure out your location.
"""

# Imports

from ctypes import windll
from datetime import datetime
from dateutil import tz
from tkinter import *
from tkinter import font as tkFont
import json
import requests
import sys
import time
import tkinter.messagebox
import urllib.request

# Fixes blurry text encountered when using display scalling.

windll.shcore.SetProcessDpiAwareness(1)

# Initialization.

app = Tk()
app.attributes('-topmost', True, '-alpha', 0.95)
app.configure(bg='#BFB9FA')
app.geometry('500x295')
app.iconbitmap('time.ico')
app.resizable(0, 0)
app.title('Ti.me')

# Miscellaneous.

button_pressed = 0
count_column = 0
monserrat_10 = tkFont.Font(family='Monserrat', size=10)

# Functions


def get_date():
    current_date = time.strftime('%a, %d %b %Y')
    date_label.config(text=current_date)
    date_label.after(200, get_date)


def get_labels():
    frame = Frame(app, bg='#BFB9FA')

    # Grid based solution that allows me to put only a specific word in bold
    # text; Label doesn't allow this out of the box.

    label_frame = Frame(frame, bg='#BFB9FA')
    label_frame.grid(row=0, column=0)

    # Allows Ti.me to be launched in the event of an exception (ie. offline,
    # timeout, etc.)

    try:

        # Ensures that a redundant Label isn't created.

        if len(dec_ip['city']) != 0:

            # Continuation of the Grid based solution.

            Label(label_frame, text='Time in ', font=('Lato', 12),
                  fg='#333333', bg='#BFB9FA').grid(row=0, column=0)

            Label(
                label_frame,
                text=dec_ip['city'] +
                ', ',
                font=(
                    'Lato',
                    12,
                    'bold'),
                fg='#333333',
                bg='#BFB9FA').grid(
                row=0,
                column=1)

            Label(label_frame, text=dec_ip['countryCode'] + ' now',
                  font=('Lato', 12), fg='#333333', bg='#BFB9FA'
                  ).grid(row=0, column=2)
    except BaseException:

        Label(label_frame, text='Time at ', font=('Lato', 12),
              fg='#333333', bg='#BFB9FA').grid(row=0, column=0)

        Label(label_frame, text='Local, ', font=('Lato', 12, 'bold'),
              fg='#333333', bg='#BFB9FA').grid(row=0, column=1)

        Label(label_frame, text='NA now', font=('Lato', 12),
              fg='#333333', bg='#BFB9FA').grid(row=0, column=2)

    # Allows the function get_time to access the variable.

    global time_label
    time_label = Label(frame, font=('Montserrat', 36, 'bold'),
                       fg='#333333', bg='#BFB9FA')
    time_label.grid(row=1, column=0)

    # Allows the function get_date to access the variable.

    global date_label
    date_label = Label(frame, font=('Lato', 12), fg='#333333',
                       bg='#BFB9FA')
    date_label.grid(row=2, column=0)

    # date_label was too close to the button_frame so I created a spacer of
    # value 1.

    spacer = Label(frame, text='', font=('Lato', 1), fg='#333333',
                   bg='#BFB9FA')
    spacer.grid(row=3, column=0)

    # Applying the same grid based solution allowing to me to align the
    # buttons in an aestetically pleasing manner.

    button_frame = Frame(frame, bg='#BFB9FA')
    button_frame.grid(row=4, column=0)

    def button(
        x,
        y,
        text,
        bcolor,
        fcolor,
        cmd,
        row,
        column,
    ):

        def on_enter(e):
            new_button['background'] = fcolor
            new_button['foreground'] = bcolor

        def on_leave(e):
            new_button['background'] = bcolor
            new_button['foreground'] = fcolor

        new_button = Button(
            button_frame,
            width=9,
            height=1,
            text=text,
            font=monserrat_10,
            fg=fcolor,
            bg=bcolor,
            border=0,
            activeforeground=fcolor,
            activebackground=bcolor,
            command=cmd,
        )
        new_button.grid(row=row, column=column)
        new_button.bind('<Enter>', on_enter)
        new_button.bind('<Leave>', on_leave)

    button(
        0,
        0,
        ' AM/PM',
        '#e0b9fa',
        '#333333',
        lambda: onclick(1),
        0,
        0,
    )
    button(
        0,
        0,
        'Search',
        '#b9fabf',
        '#333333',
        lambda: onclick(2),
        0,
        1,
    )
    button(
        0,
        0,
        'About ',
        '#b9d4fa',
        '#333333',
        lambda: onclick(3),
        0,
        2,
    )

    frame.pack(expand=True)


def get_location():
    try:
        ip_api = 'http://ip-api.com/json/'
        request_ip = urllib.request.Request(ip_api)
        ip = urllib.request.urlopen(request_ip, timeout=1).read()
        global dec_ip
        dec_ip = json.loads(ip.decode('utf-8'))
    except urllib.error.URLError:
        None


def get_time():
    from_zone = tz.gettz('UTC')
    try:
        to_zone = tz.gettz(dec_ip['timezone'])
    except NameError:
        to_zone = tz.gettz('local')
    utc_now = datetime.utcnow()
    utc = utc_now.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)
    if button_pressed == 0:
        time_now = local.strftime('%H:%M:%S')
    if button_pressed != 0:
        time_now = local.strftime('%I:%M %p')
    time_label.config(text=time_now)
    time_label.after(200, get_time)


def onclick(args):
    if args == 1:
        global button_pressed
        if button_pressed == 0:
            button_pressed = 1
        elif button_pressed != 0:
            button_pressed = 0
    if args == 2:
        top = Toplevel(app)
        top.geometry("500x250")
        top.title("Search")
        top.attributes('-topmost', True, '-alpha', 0.95)
        top.configure(bg='#BFB9FA')
        top.iconbitmap('time.ico')
        top.resizable(0, 0)

        frame = Frame(top, bg='#BFB9FA')
        label_frame = Frame(frame, bg='#BFB9FA')
        label_frame.grid(row=0, column=0)

        Label(label_frame, text='Type in the city below', font=('Lato', 12),
              fg='#333333', bg='#BFB9FA').grid(row=0, column=0)

        spacer = Label(frame, text='', font=('Lato', 1), fg='#333333',
                       bg='#BFB9FA')
        spacer.grid(row=1, column=0)

        entry = Entry(frame, font=('Lato', 12), justify='center')
        entry.grid(row=2, column=0)

        spacer = Label(frame, text='', font=('Lato', 1), fg='#333333',
                       bg='#BFB9FA')
        spacer.grid(row=3, column=0)

        button_frame = Frame(frame, bg='#BFB9FA')
        button_frame.grid(row=4, column=0)

        def button(
            x,
            y,
            text,
            bcolor,
            fcolor,
            cmd,
            row,
            column,
        ):

            def on_enter(e):
                new_button['background'] = fcolor
                new_button['foreground'] = bcolor

            def on_leave(e):
                new_button['background'] = bcolor
                new_button['foreground'] = fcolor

            new_button = Button(
                button_frame,
                width=9,
                height=1,
                text=text,
                font=monserrat_10,
                fg=fcolor,
                bg=bcolor,
                border=0,
                activeforeground=fcolor,
                activebackground=bcolor,
                command=cmd,
            )
            new_button.grid(row=row, column=column)
            new_button.bind('<Enter>', on_enter)
            new_button.bind('<Leave>', on_leave)

        button(
            0,
            0,
            'Find',
            '#f4fab9',
            '#333333',
            lambda: onclick(4),
            0,
            0,
        )

        frame.pack()

        top.mainloop()

    if args == 3:
        tkinter.messagebox.showinfo('About',
                                    'Ti.me [v0.9.0]\n@bigTajine')

    if args == 4:
        tkinter.messagebox.showinfo('Note',
                                    'This function isn\'t avaliable')


# Calling the functions below to allow for more order and oversight.

get_location()
get_labels()
get_time()
get_date()

app.mainloop()
