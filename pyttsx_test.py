#!/usr/bin/python

import pyttsx

speakEngine = pyttsx.init()
rate = speakEngine.getProperty('rate')
speakEngine.setProperty('rate', rate-100)
#voices = speakEngine.getProperty('voices')
#speakEngine.setProperty('voice', voices[1].id)
speakEngine.say("You have "+str(self.Tetris_Points)+" points")
speakEngine.runAndWait()