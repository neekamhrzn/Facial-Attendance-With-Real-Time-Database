# **Facial Attendance with Real-Time Database Integration**
This project is aimed at developing a facial recognition-based attendance system integrated with a real-time database. The system captures live video feed, detects faces, and verifies them against a database of stored images. Upon successful verification, the attendance is recorded in the database along with the timestamp. The system is built using Python and utilizes the following technologies:

* OpenCV for capturing video feed and face detection
* DeepFace library for facial recognition
* Pyrebase for integrating with the Firebase real-time database

## **Installation**
* Clone this repository to your local machine.
* Install the required Python libraries:
  
 `pip install opencv-python deepface pyrebase`
* Ensure you have a Firebase account and set up a real-time database.
* Update the Firebase configuration in the code (config dictionary).

## **Usage**
* Prepare a folder (attendance_project/people) containing images of individuals whose attendance you want to track.
* Run the script my_project.py.
* The system will display live video feed with face detection. When a face is detected and verified against the database, the attendance will be recorded in real-time.
* Press 'q' to exit the application.

