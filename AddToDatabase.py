import pyrebase
from datetime import datetime

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

data={
    "101":{"firstName":"elon", "lastName":"musk","subject":"physics"},
    "202":{"firstName":"kylie", "lastName":"jenner","subject":"chemistry"},
    "303":{"firstName":"mukesh", "lastName":"ambani","subject":"biology"},
    "404":{"firstName":"nita", "lastName":"ambani","subject":"astronomy"},
    "505":{"firstName":"mark", "lastName":"zuckerberg","subject":"accounts"},
    "606":{"firstName":"jeff", "lastName":"bezos","subject":"computer"},
    "707":{"firstName":"bill", "lastName":"gates","subject":"physics"}
}

#run only once
# db.child("Students").set(data)


# #set last attendance time and total number of attendance

# t=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# db.child("Students").child("101").update({"lastAttendanceTime":t,"totalAttendance":"0"})
# db.child("Students").child("202").update({"lastAttendanceTime":t,"totalAttendance":"0"})
# db.child("Students").child("303").update({"lastAttendanceTime":t,"totalAttendance":"0"})
# db.child("Students").child("404").update({"lastAttendanceTime":t,"totalAttendance":"0"})
# db.child("Students").child("505").update({"lastAttendanceTime":t,"totalAttendance":"0"})
# db.child("Students").child("606").update({"lastAttendanceTime":t,"totalAttendance":"0"})
# db.child("Students").child("707").update({"lastAttendanceTime":t,"totalAttendance":"0"})


#-------------------------------------retrieve data to update---------------------------------------
#----------------------------------this code is only for testing------------------------------------
#we have id by student_ids[ind]

id=606
stu=db.child("Students").child(str(id)).get()
print("student info : ",stu.val())
lastAttendanceTimeToObject=datetime.strptime(stu.val()["lastAttendanceTime"],"%Y-%m-%d %H:%M:%S")
print(lastAttendanceTimeToObject)
currentTimeObject=datetime.now()
currentTimeToStr=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
elapsedTime=(currentTimeObject-lastAttendanceTimeToObject).total_seconds()
totalAttendance=int(stu.val()["totalAttendance"])
totalAttendance+=1
print("elapsed time: ",elapsedTime)
db.child("Students").child(str(id)).update({"lastAttendanceTime":datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "totalAttendance":str(totalAttendance)})

