#!/usr/bin/python

from mytetris2 import *

tetrisgame = RGB_Tetris("mace")
tetrisgame.startTable()

while True:
	try:
		pass
	except:
		tetrisgame.running = False
		