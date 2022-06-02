from django.shortcuts import redirect, render
import pyrebase
import cv2
import os
import datetime
from PIL import Image
import numpy as np
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc
from django.http import  StreamingHttpResponse
from NCKH.settings import MEDIA_URL, MEDIA_ROOT
from django.contrib import messages
from website import FCMManager as fcm


config = {
  'apiKey': "AIzaSyA1W3abFBkqf0uX0ibIVZZsdmASdClR3Qk",
  'authDomain': "face-database-5fd0c.firebaseapp.com",
  'projectId': "face-database-5fd0c",
  'databaseURL' : "https://face-database-5fd0c-default-rtdb.asia-southeast1.firebasedatabase.app",
  'storageBucket': "face-database-5fd0c.appspot.com",
  'messagingSenderId': "898599541632",
  'appId': "1:898599541632:web:0e9550ee7801541566ff65",
  'measurementId': "G-YZWFBB170J",
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()


#lop = database.child('Nhandien').shallow().get().val()
#print(lop)
#for i in lop:
#print(database.child('Nhandien').child('DI18V7F1').child("1812964").child('Hocsinh').child('Ten').get().val())
# for i in lop:
#     if database.child('Nhandien').child(i).child("B1812964").child('Hocsinh').child('Ten').get().val():
#         get = database.child('Nhandien').child(i).child("B1812964").child('Hocsinh').child('Ten').get().val()
#         print(get)
#         break

now = datetime.datetime.now()
date = now.date()

vao = database.child('Diemdanh').child(date).child('1812964').child('Vao').get().val()
ra = database.child('Diemdanh').child(date).child('1812964').child('Ra').get().val()

print(ra)
# if ra!=None:
#     print("Da Vao")
