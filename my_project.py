import cv2
import os 
from deepface import DeepFace
import threading
import pyrebase
from datetime import datetime

# Get current date and time
current_date_time = datetime.now()
current_date = current_date_time.date()  # Extract date

#for database
config={
    "apiKey": "AIzaSyCumqnQCEQ10Ab0pE103Y4PgeEm-fY66eo",
    "authDomain": "demodb-35b2b.firebaseapp.com",
    "projectId": "demodb-35b2b",
    "databaseURL":"https://demodb-35b2b-default-rtdb.firebaseio.com/",
    "storageBucket": "demodb-35b2b.appspot.com",
    "messagingSenderId": "1002446830137",
    "appId": "1:1002446830137:web:e7864fe9532d58a3c22be8",
    "measurementId": "G-JFQ91J5ZS8"
}

firebase=pyrebase.initialize_app(config)
db=firebase.database()


#initialize variables
face_verified=False
counter=0 
ind=0   # index of verified face to find roll

#background image for graphics
bg_img=cv2.imread("attendance_project/background_images/mybg.png")
bg_img=cv2.resize(bg_img,(1050,775))
original_bg_img = bg_img.copy()  # Store a copy of the original image
video_cap=cv2.VideoCapture(0)

#adjust height and width of video capture frame , i.e. camera
frame_width = 320
frame_height = 240
video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
face_cap=cv2.CascadeClassifier("C:/Users/DELL/AppData/Local/Programs/Python/Python310/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")

image_folder_path="attendance_project/people"
images=[]
student_ids=[]
for file in os.listdir(image_folder_path):
    img=cv2.imread(os.path.join(image_folder_path,file))
    images.append(img)
    id=file.split('.')[0]
    student_ids.append(id)


#main function to verify faces
def face_verify(video_data):
    global face_verified
    global ind
    try:
        for org_pic in images:
            if(DeepFace.verify(video_data,org_pic.copy())['verified']):
                face_verified=True
                ind=images.index(org_pic)
                print("face verified.....",ind)

                # update totalAttendance and lastAttendanceTime in database
                stu=db.child("Students").child(str(student_ids[ind])).get()
                print("student info : ",stu.val())
                lastAttendanceTimeToObject=datetime.strptime(stu.val()["lastAttendanceTime"],"%Y-%m-%d %H:%M:%S")
                currentTimeObject=datetime.now()
                elapsedTime=(currentTimeObject-lastAttendanceTimeToObject).total_seconds()
                totalAttendance=int(stu.val()["totalAttendance"])
                totalAttendance+=1
                print("elapsed time: ",elapsedTime)
                if elapsedTime>60: 
                    db.child("Students").child(str(student_ids[ind])).update({"lastAttendanceTime":datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "totalAttendance":str(totalAttendance)})
            
                break
            else:
                face_verified=False

    except ValueError:
        face_verified=False
        print("face not verified.....")



# display frames
while True:

    ret , video_data=video_cap.read()

    if ret:
        if(counter%30 == 0):
            try:
                threading.Thread(target=face_verify(video_data),args=(video_data.copy())).start()
            except ValueError:
                pass
        counter+=1

    gray_video=cv2.cvtColor(video_data,cv2.COLOR_BGR2GRAY)
    faces=face_cap.detectMultiScale(gray_video,1.1,5,minSize=(30,30))
    
    if face_verified:
        bg_img = original_bg_img.copy()
        for (x,y,w,h) in faces:
            cv2.rectangle(video_data,(x,y),(x+w,y+h),(0,225,0),3)

        stu=db.child("Students").child(str(student_ids[ind])).get()
        cv2.putText(bg_img,"Face verified",(645,330),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,225,0),2)
        cv2.putText(bg_img,"{}".format(student_ids[ind]),(290,565),cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,255,255),2)
        cv2.putText(bg_img,"{}".format(stu.val()["firstName"]),(485,565),cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,255,255),2)
        cv2.putText(bg_img,"{}".format(stu.val()["subject"]),(675,565),cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,255,255),2)
        cv2.putText(bg_img,"Date: {}".format(current_date),(250,650),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),2)



    
    else:
        bg_img = original_bg_img.copy()
        for(x,y,w,h) in faces:
            cv2.rectangle(video_data,(x,y),(x+w,y+h),(0,0,225),3)
        cv2.putText(bg_img,"Not detected",(645,330),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,225),2)
        cv2.putText(bg_img,"Date: {}".format(current_date),(250,650),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),2)



    bg_img[200:200+240,270:270+320]=video_data
    cv2.imshow("Attendance System",bg_img)

    #to exit
    if cv2.waitKey(10)==ord('q'):
        break

