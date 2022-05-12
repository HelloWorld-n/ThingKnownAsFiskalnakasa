#!/bin/python3
import tkinter as Tk
import platform
import os

__DIGITS = "0123456789"
__UPCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
__DOWNCASE = "abcdefghijklmnopqrstuvwxyz"
__ALPHABET = __UPCASE + __DOWNCASE
__DIGITS = "0123456789"
__OPERATORS = "+-*/%↑"

# Dark mode, very usefull
if platform.system() == "Linux":
	import subprocess
	def theme():
		try:
			out = subprocess.run(
				['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'],
				capture_output = True,
			)
			stdout = out.stdout.decode()
		except Exception:
			return 'Light'
		theme = stdout.lower().strip()[1:-1]
		if theme.endswith('-dark'):
			return "Dark"
		else:
			return "Light"

elif platform.system() == "Windows":
	from winreg import HKEY_CURRENT_USER as hkey, QueryValueEx as getSubkeyValue, OpenKey as getKey
	
	def theme():
		valueMeaning = {0: "Dark", 1: "Light"}
		key = getKey(hkey, "Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize")
		subkey = getSubkeyValue(key, "AppsUseLightTheme")[0]
		return valueMeaning[subkey]

elif platform.system in ["Darwin", "Mac"]:
	import ctypes
	import ctypes.util

	def theme():

		appkit = ctypes.cdll.LoadLibrary(ctypes.util.find_library('AppKit'))
		objc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('objc'))

		void_p = ctypes.c_void_p
		ull = ctypes.c_uint64

		objc.objc_getClass.restype = void_p
		objc.sel_registerName.restype = void_p
		objc.objc_msgSend.restype = void_p
		objc.objc_msgSend.argtypes = [void_p, void_p]

		msg = objc.objc_msgSend
		def _utf8(s):
			if not isinstance(s, bytes):
				s = s.encode('utf8')
			return s

		def n(name):
			return objc.sel_registerName(_utf8(name))

		def C(classname):
			return objc.objc_getClass(_utf8(classname))
		NSAutoreleasePool = objc.objc_getClass('NSAutoreleasePool')
		pool = msg(NSAutoreleasePool, n('alloc'))
		pool = msg(pool, n('init'))

		NSUserDefaults = C('NSUserDefaults')
		stdUserDef = msg(NSUserDefaults, n('standardUserDefaults'))

		NSString = C('NSString')

		key = msg(NSString, n("stringWithUTF8String:"), _utf8('AppleInterfaceStyle'))
		appearanceNS = msg(stdUserDef, n('stringForKey:'), void_p(key))
		appearanceC = msg(appearanceNS, n('UTF8String'))

		if appearanceC is not None:
			out = ctypes.string_at(appearanceC)
		else:
			out = None

		msg(pool, n('release'))

		if out is not None:
			return out.decode('utf-8')
		else:
			return 'Light'
			
else: # Unable to test.
	def theme():
		return None

def isSystemDark():
    return theme() == "Dark"

def isSystemLight():
	return theme() == "Light"


global COLORS_DARK, COLORS, COLORS_LIGHT

COLORS_LIGHT = {
	"bg": "#D0D0CC",
	"fg": "#282833",
	"bg-plus": "#978BC8",
	"bg-key": "#E0E0E0",
	"bg-key-digit": "#D9AAFF",
	"bg-key-function": "#BBF8BB",
	"bg-key-variable": "#F8DAAC",
	"bg-key-expression": "#EEFC9F",
	"bg-key-state": "#ACDCF8",
	"bg-key-command": "#F8ACD2",
	"fg-red": "#AA0033",
	"fg-orange": "#BF6F00",
	"fg-yellow": "#9BA400",
	"fg-green": "#009F28",
	"fg-cyan": "#0077B0",
	"fg-blue": "#6100B0",
	"fg-purple": "#9D00AE",
}

COLORS_DARK = {
	"bg": "#282833",
	"fg": "#D0D0CC",
	"bg-plus": "#362C5D",
	"bg-key": "#2B2B2B",
	"bg-key-digit": "#270047",
	"bg-key-function": "#095509",
	"bg-key-variable": "#754B0A",
	"bg-key-expression": "#918503",
	"bg-key-state": "#084263",
	"bg-key-command": "#740A3F",
	"fg-red": "#DD4A77",
	"fg-orange": "#FFB54D",
	"fg-yellow": "#F4FF36",
	"fg-green": "#41FF71",
	"fg-cyan": "#55C8FF",
	"fg-blue": "#B050FF",
	"fg-purple": "#ED4CFF",
}


def setColorMode(isItLight = None, changeSettings = True):
	global COLORS_DARK, COLORS, COLORS_LIGHT
	if isItLight == False:
		COLORS = COLORS_DARK
	elif isItLight == None:
		COLORS = COLORS_LIGHT if isSystemLight() else COLORS_DARK 
	elif isItLight == True:
		COLORS = COLORS_LIGHT
	else:
		generateMessage(
			"There is an error in reading settings for color mode.\n"
			"System will switch to default.\n"
		)
		setColorMode(None)
	
	if changeSettings:
		file = open(f"./.settings/theme.pyon", "w")
		file.write(f"{isItLight}")
		file.close()


def theAppFont(name = "Consolas", size = "12", style = "normal"):
	return f"{name} {size} {style}"

def createElement(element, *args, toPack = True, **kwargs):
	if "font" not in kwargs.keys() and element not in [Tk.Canvas, Tk.Frame]:
		kwargs["font"] = theAppFont()
	if "bg" not in kwargs.keys():
		kwargs["bg"] = COLORS["bg"]
	if "fg" not in kwargs.keys() and "foreground" not in kwargs.keys():
		kwargs["fg"] = COLORS["fg"]
	try:
		result = element(*args, **kwargs)
	except Tk.TclError:
		del(kwargs["fg"])
		result = element(*args, **kwargs)
	
	if toPack:
		result.pack()
	return result


def gridElement(element, *args, row, column, rowspan = 1, columnspan = 1, **kwargs):
	result = createElement(element, *args, toPack = False, **kwargs)
	result.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan)
	return result

# Može se koristiti da obavesti korisnika o potencialnim problemima
def generateMessage(message):
	infoMessage = Tk.Tk()
	infoMessage.configure(bg = COLORS["bg"])
	lbl = gridElement(
		Tk.Label, infoMessage,
		row = 0, column = 0,
		text = message,
		bg = COLORS["bg"], fg = COLORS["fg"],
		padx = 5, pady = 5,
	)
	infoMessage.mainloop()


try:
	file = open("./.settings/theme.pyon", "r")
	setColorMode(eval(file.read()))
	file.close()
except FileNotFoundError:
	os.mkdir("./.settings")
	setColorMode(None)
