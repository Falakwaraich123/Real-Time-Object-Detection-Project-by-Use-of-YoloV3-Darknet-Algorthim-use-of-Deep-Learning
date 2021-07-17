from weakref import WeakMethod
from flask import Flask,jsonify
from flask import render_template, redirect, url_for
from flask import Response, request
from yolov3 import VideoCamera
import database as db
import time
import cv2
from datetime import date
import time
from pathlib import Path
app = Flask(__name__)
database = "MyDB.db"

@app.route('/')
def index():
    return render_template('v2_auth.html')

@app.route('/SignUp', methods = ['POST', 'GET'])
def SignUp():
    if request.method == 'POST':
        email = request.form['email']
        psw = request.form['psw']
        re_psw = request.form['psw-repeat']
        # print("Email : ", email, "\n Pass : ", psw)
        if psw == re_psw:
            user_info = (email, psw)
            db.writeUsers_Table(database, user_info )
            return render_template('v2_auth.html', warn ='Data Added')
        else:
            return render_template('v2_auth.html', warn = "Password Does Not Matched")
    
@app.route('/SignIn', methods = ['POST', 'GET'])
def SignIn():
    if request.method == 'POST':
        email = request.form['email']
        psw = request.form['psw']
        user_info = (email,psw)
        if db.userExists(database, user_info):
            return render_template('index.html', user = email)
        else:
            return render_template('v2_auth.html', warn = "Wrong Info")
@app.route('/SignOut', methods = ['POST', 'GET'])
def SignOut():
    return render_template('v2_auth.html', warn = "")

@app.route('/getLogsData', methods = ['POST', 'GET'])
def getLogsData():
    logsData = db.get_logs_data(database)
    # print(logsData)
    return jsonify(logsData)

def gen(yolo):
    start_time = time.time()
    while True:
        gframe, frame, label, confidence, fps, t= yolo.get_detect()
        time_went =time.time() - start_time 
        if  time_went>10:
            start_time = time.time()
            today = date.today()
            t = time.strftime("%H_%M_%S")
            d = today.strftime("%b_%d_%Y")
            time_name = str(d) + "_" + str(t)
            
            Path("static/Dataset_images").mkdir(parents=True, exist_ok=True)

            file_name = "static/Dataset_images/" + str(time_name) + label + '.png'
            cv2.imwrite(file_name,frame)
            log_info = (file_name, label, str(round(confidence, 2)), str(round(fps, 2)), str(t))
            db.writeLogs_Table("MyDB.db", log_info)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + gframe + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    db.makeTables(database)
    app.run(debug=True)