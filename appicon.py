#!/usr/bin/python3
#
# SUSI.AI tray icon
# on start:
#  - start susi server
#  depending on config (to be done, where?)
#  - start susi etherpad
#  - start susi voice
#
# menu items:
#  - toggle susi voice recognition
#  - toggle susi etherpad
#  - configure
#  - about
#  - exit
# status display
# [ ] susi server running
# [ ] susi etherpad running
# [ ] susi voice recognition running

import pystray
import sys
import os
from pystray import Menu as menu, MenuItem as item
from PIL import Image, ImageDraw

from susi_linux.ui import ConfigurationWindow

susi_voice_enabled = False
susi_pad_enabled = False

def on_susi_voice_clicked(icon, item):
    global susi_voice_enabled
    susi_voice_enabled = not item.checked
    if susi_voice_enabled:
        os.system("susi-linux start")
    else:
        os.system("susi-linux stop")
def on_susi_pad_clicked(icon, item):
    global susi_pad_enabled
    susi_pad_enabled = not item.checked
    if susi_pad_enabled:
        os.system("susi-etherpad start")
    else:
        os.system("susi-etherpad stop")
def on_configure_clicked(icon, item):
    window = ConfigurationWindow()
    window.show_window()
def on_about_clicked(icon, item):
    print("TODO need to display about dialog")
def on_exit_clicked(icon, item):
    os.system("susi-assistant stop")
    sys.exit(0)

def create_image():
    width = height = 100
    color1 = "red"
    color2 = "blue"
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

icon = pystray.Icon('SUSI.AI', create_image(), menu=menu(
    item('SUSI.AI', action = lambda item: item),
    item(
        'Voice Assistant',
        on_susi_voice_clicked,
        checked = lambda item: susi_voice_enabled),
    item(
        'Skill Pad',
        on_susi_pad_clicked,
        checked = lambda item: susi_pad_enabled),
    item(
        'Configure',
        on_configure_clicked),
    item(
        'About',
        on_about_clicked),
    item(
        'Exit',
        on_exit_clicked),
    ))

os.system("susi-server start")
icon.run()

