import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://faceattendance-f26c7-default-rtdb.firebaseio.com/"})

ref=db.reference('Students')
data={
    "2105527":
    {
        "Name":"Anviksha Singh",
        "Branch":"CSE",
        "Standing":"G",
        "Starting Year":2021,
        "Year":"Third",
        "Total_Attendance":9,
        "Last_Attendance_Time":"2023-10-5 20:12:23"
        
    },
   "2105536":
    {
        "Name":"Ayush Singh",
        "Branch":"CSE",
        "Standing":"G",
        "Starting Year":2021,
        "Year":"Third",
        "Total_Attendance":6,
        "Last_Attendance_Time":"2023-10-5 12:12:23"
        
    },
    "2105563":
    {
        "Name":"Priyanshu Singh",
        "Branch":"CSE",
        "Standing":"G",
        "Starting Year":2021,
        "Year":"Third",
        "Total_Attendance":8,
        "Last_Attendance_Time":"2023-10-5 21:12:1"
        
    }
}
for key,value in data.items():
    ref.child(key).set(value)