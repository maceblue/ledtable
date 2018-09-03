#!/usr/bin/python

from mytetris2 import *


while True:
    try:
        tetrisgame =RGB_Tetris(s,"mace")
        tetrisgame.startGame()
    except: 
        pass