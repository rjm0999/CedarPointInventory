import tkinter as tk
import math
import pandas as pd
from datetime import date, datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


FONT = "Consolas"
DEPARTMENTS = pd.read_csv("database/Departments.csv", index_col="Dept #")


"""
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
import tkinter as tk


FR_PRIVATE = 0X10
FR_NOT_ENUM = 0X20

def loadfont(fontpath, private=True, enumerable=False):
    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else: raise TypeError('fontpath must be of type str or unicode')
    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)


FONT = "Consolas"
FONT = "ComicMono" if loadfont("database/ComicMono.ttf") else "Consolas"
"""
