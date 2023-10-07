import cv2
import os
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://faceattendance-f26c7-default-rtdb.firebaseio.com/",
                                    'storageBucket':"faceattendance-f26c7.appspot.com"})



#importting student images

folderpath="StudentImg"

pathlist=os.listdir(folderpath)
print(pathlist)

imgList=[]
studentIds=[]

for path in pathlist:
    imgList.append(cv2.imread(os.path.join(folderpath,path)))
    studentIds.append(os.path.splitext(path)[0])

    #to send or upload the images of the student to the Storage of the Database
    fileName=f'{folderpath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)


print(studentIds)
def findEncoding(imagesList):
    encodeList=[]
    for img in imagesList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
print("Encoding Started")
encodeListKnown=findEncoding(imgList)
encodeListKnownWithIds=[encodeListKnown,studentIds]
print("encoding complete")      

file=open('EncodeFile.p','wb')
pickle.dump(encodeListKnownWithIds,file)

file.close()
print("File Saved")