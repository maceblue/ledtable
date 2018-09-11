#!/usr/bin/python

import pyttsx

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)
voices = engine.getProperty('voices')
for voice in voices:
   print(voice.id)
   engine.setProperty('voice', 'german')
   engine.say('Du hast 120 Punkte.')
   #engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()
#speakEngine.setProperty('voice', voices[1].id)
#engine.say("You have 1345 points")
#engine.runAndWait()
