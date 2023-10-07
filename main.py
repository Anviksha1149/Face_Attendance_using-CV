import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://faceattendance-f26c7-default-rtdb.firebaseio.com/",
                                    'storageBucket':"faceattendance-f26c7.appspot.com"})



bucket=storage.bucket()
cap=cv2.VideoCapture(0)#capturing the images through  one webcam
cap.set(3,640)#setting the width of the web cam
cap.set(4,480)#setting the height

imgBackground=cv2.imread("background.png") 
folderModePath="Modes"
modepathlist=os.listdir(folderModePath)
imgModeList=[]

for path in modepathlist:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

 #load the encoding file
print("Loading the encoded file")
file=open('EncodeFile.p','rb')
encodeListKnownWithIds=pickle.load(file)
file.close()
encodeListKnown,studentIds=encodeListKnownWithIds
#print(studentIds)
print("Encoded file is loaded")
modeType=0
counter=0
id=-1
imgStudent=[]


while True:
    success,img=cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    FaceCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS,FaceCurFrame)


    imgBackground[162:162+480,55:55+640]=img #overlaping the background frame with webcam video
    imgBackground[44:44+633,808:808+414]=imgModeList[modeType]


    #cv2.imshow("webcam",img)
    for encodeface,faceloc in zip(encodeCurFrame,FaceCurFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeface)
        faceDis=face_recognition.face_distance(encodeListKnown,encodeface)
       # print("matches",matches)
        #print("faceDis",faceDis)
        matchIndex=np.argmin(faceDis) 
        if matches[matchIndex]:
            y1,x2,y2,x1=faceloc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            bbox=55+x1,162+y1,x2-x1,y2-y1
            imgBackground=cvzone.cornerRect(imgBackground,bbox,rt=0)
            id=studentIds[matchIndex]
            
            
            if counter==0:
                
                counter=1
                modeType=1
              
    if counter!=0:
        
        if counter==1:
            print("Downloading the info")
            #getting data from the database
            studentInfo=db.reference(f'Students/{id}').get()
            print(studentInfo)
            #getting image from the database
            blob=bucket.get_blob(f'StudentImg/{id}.jpg')
            array=np.frombuffer(blob.download_as_string(),np.uint8)
            imgStudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
            
        cv2.putText(imgBackground,str(studentInfo['Total_Attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        cv2.putText(imgBackground,str(studentInfo['Branch']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)    
        cv2.putText(imgBackground,str(id),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
        cv2.putText(imgBackground,str(studentInfo['Standing']),(910,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
        cv2.putText(imgBackground,str(studentInfo['Year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
        cv2.putText(imgBackground,str(studentInfo['Starting Year']),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
        (w,h), _ = cv2.getTextSize(studentInfo['Name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
        offset=(414-w)//2
        cv2.putText(imgBackground,str(studentInfo['Name']),(808+offset,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
        #imgBackground[175:175+216,909:909+216]=imgStudent

        counter+=1

         
    cv2.imshow("Face attendance",imgBackground)
    cv2.waitKey(1)
