#!/usr/bin/python3

import pystray
import sys
import os
from pystray import Menu as menu, MenuItem as item
from PIL import Image, ImageDraw

susi_enabled = False

def on_susi_clicked(icon, item):
    global susi_enabled
    susi_enabled = not item.checked
def on_exit_clicked(icon, item):
    os.system("susi-assistant stop")
    sys.exit(0)
def on_start_etherpad(icon, item):
    os.system("susi-etherpad start")


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
    item(
        'Enable SUSI.AI Voice Assistant',
        on_susi_clicked,
        checked = lambda item: susi_enabled),
    item(
        'Exit SUSI.AI',
        on_exit_clicked),
    item(
        'Start SkillPad',
        on_start_etherpad)
    ))

icon.run()
