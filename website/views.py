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
from NCKH.settings import BASE_DIR, MEDIA_URL, MEDIA_ROOT
from django.contrib import messages
from website import FCMManager as fcm


# Create your views here.

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

def home(request):
    return render(request, 'home.html')

def getRegisterHS(request):
    list = database.child('Nhandien').shallow().get().val()
    return render(request, 'registerHS.html',{'list':list})

def getRegisterPH(request):
    lop = database.child('Nhandien').shallow().get().val()
    list = []
    for i in lop:
        hs = database.child('Nhandien').child(i).shallow().get().val()
        list.append(hs)

    return render(request, 'registerPH.html',{'list':list,'lop':lop})

def postRegisterHS(request):
    type = 'HS'
    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        lop = request.POST.get('lop')
        ngaysinh = request.POST.get('ngaysinh')

    database.child('Nhandien').child(lop).child(id).child('Hocsinh').child('Ten').set(name)
    database.child('Nhandien').child(lop).child(id).child('Hocsinh').child('Ngaysinh').set(ngaysinh)
    
    messages.success(request, "Them HS thanh cong...")

    scanface(id,type)
    return redirect('home')

def postRegisterPH(request):
    type = 'PH'
    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        lop = request.POST.get('lop')
        ngaysinh = request.POST.get('ngaysinh')
        sdt = request.POST.get('sdt')

    database.child('Nhandien').child(lop).child(id).child('Phuhuynh').child('Ten').set(name)
    database.child('Nhandien').child(lop).child(id).child('Phuhuynh').child('Ngaysinh').set(ngaysinh)
    database.child('Nhandien').child(lop).child(id).child('Phuhuynh').child('Sodienthoai').set(sdt)

    scanface(id,type)
    return redirect('home')

def scanface(id,type):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    count = 0
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 3)
            count += 1
            
            if(os.path.exists(MEDIA_ROOT.replace("\\", "/") + 'images/')):
                cv2.imwrite(MEDIA_ROOT.replace("\\", "/") + 'images/User.' + str(type) +'.'+ str(id) + '.' + str(count) + '.jpg' , gray[y: y+h, x :x+w])
            else:
                os.makedirs(MEDIA_ROOT.replace("\\", "/") + 'images')
                cv2.imwrite(MEDIA_ROOT.replace("\\", "/") + 'images/User.' + str(type) +'.'+ str(id) + '.' + str(count) + '.jpg' , gray[y: y+h, x :x+w])

                
        cv2.imshow('img', frame)
        
        cv2.waitKey(1)

        if count > 99:
            break

    cap.release()
    cv2.destroyAllWindows()

def getImageWithID():
    imagePaths = [os.path.join(MEDIA_ROOT.replace("\\", "/") + 'images', f) for f in os.listdir(MEDIA_ROOT.replace("\\", "/") + 'images')]

    faces = []
    ids = []

    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        id = int(imagePath.split('.')[2])
        faces.append(faceNp)
        ids.append(id)

        cv2.imshow('training', faceNp)
        cv2.waitKey(10)
    return faces, ids

def gettrainning(request):
    trainning()
    return render(request, 'home.html')

def trainning():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = getImageWithID()
    recognizer.train(faces, np.array(ids))
    
    if(os.path.exists(MEDIA_ROOT.replace("\\", "/") + 'recognizer/')):
        recognizer.write(MEDIA_ROOT.replace("\\", "/") + 'recognizer/trainningData.yml')
    else:
        os.mkdir(MEDIA_ROOT.replace("\\", "/") + 'recognizer/')
        recognizer.write(MEDIA_ROOT.replace("\\", "/") + 'recognizer/trainningData.yml')
        


def getProfile(id):
    lop = database.child('Nhandien').shallow().get().val()
    for i in lop:
        if database.child('Nhandien').child(i).child(id).child('Hocsinh').child('Ten').get().val():
            get = database.child('Nhandien').child(i).child(id).child('Hocsinh').child('Ten').get().val()
            break
    return get

# Check da vao hay chua ----------------------------------------------------------------------------------
def getProfilee(id):
    lop = database.child('Nhandien').shallow().get().val()
    now = datetime.datetime.now()
    date = now.date()
    for i in lop:
        if database.child('Nhandien').child(i).child(id).child('Hocsinh').child('Ten').get().val():
            if database.child('Diemdanh').child(date).child(id).child('Vao').get().val()!=None:
                get = "Da Diem Danh"
                break
            else:
                get = database.child('Nhandien').child(i).child(id).child('Hocsinh').child('Ten').get().val()
                break
    return get



def getdetect(request):
    if request.method == 'GET':
        type =  request.GET.get('type')
    detect(type)
    return render(request, 'home.html')

def detect(type):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read(MEDIA_ROOT.replace("\\", "/") + 'recognizer/trainningData.yml')

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    fontface = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray)

        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+h]

            id, confidence = recognizer.predict(roi_gray)
            if confidence < 40:
                profile = getProfilee(id)
                if(profile != None):
                    if type == "PH":
                        cv2.putText(frame, "PH :" + str(profile) , (x+10, y+h+30), fontface, 1, (0, 255, 0), 1)
                    else:      
                        cv2.putText(frame, "HS :" + str(profile) , (x+10, y+h+30), fontface, 1, (0, 255, 0), 1)
                        now = datetime.datetime.now()
                        date = now.date()
                        time = now.time().strftime("%H:%M:%S")
                        tokens = ['fAMH085nRK-8eIEi6BNAHV:APA91bFmmx7U68lDVFIBMbClzi8BrpGCyhIbLh5L8JAs2RXr4uzDsfItCjufA7HE6vBf-9CVEsnpc9OseSJhofou7sKxN5dHEZNVh3dYV0YqxBYmmsLFIhDIMMxvzOs5eKb1ey_hmsvU']
                        fcm.sendPush("Hello " + profile, "Da vao lop: " + time, tokens)
                    
                    savetime(id,type)
            else:
                cv2.putText(frame, "Unknow", (x+10, y+h+30), fontface, 1, (0, 0, 255), 1)

        cv2.imshow('image', frame)
        if(cv2.waitKey(1) == ord('q')):
            break
                
    cap.release()
    cv2.destroyAllWindows()

def savetime(id,type):
    now = datetime.datetime.now()
    date = now.date()
    time = now.time().strftime("%H:%M:%S")
    if type == "PH":
        push = database.child('Diemdanh').child(date).child(id).child('Ra').set(str(time))
    else:
        push = database.child('Diemdanh').child(date).child(id).child('Vao').set(str(time))

# Streaming on web
def stream_view(request):
    return render(request, 'stream.html')

#bắt ngoại lệ đặt tên file media
def stream():
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time().strftime("%H-%M-%S")

    if(os.path.exists(MEDIA_ROOT + "/video/" + str(date))):
        video = cv2.VideoWriter(MEDIA_ROOT.replace("\\", "/") + "video/" + str(date) +"/demo.mp4",cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (640, 480))
    else:
        os.makedirs(MEDIA_ROOT + "/video/" + str(date))
        video = cv2.VideoWriter(MEDIA_ROOT.replace("\\", "/") + "video/" + str(date) +"/demo.mp4",cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (640, 480))

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            video.write(frame)
            cv2.imwrite('demo.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')
    except:
        storage.child(str(date)).child("demo.mp4").put('demo.mp4')

    # os.remove("demo.jpg")
    # os.remove("demo.mp4")
    cap.release()
    video.release()
    cv2.destroyAllWindows()

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')

def test(request):
    return render(request, 'test.html',{'media_root':MEDIA_ROOT.replace("\\", "/"),
                                        'media_url':MEDIA_URL,
                                        'base_dir':BASE_DIR})

def dsdd(request):
    date = database.child('Diemdanh').shallow().get().val()
    list = database.child('Diemdanh').get()
    return render(request, 'dsdd.html',{'date':date,'list':list})