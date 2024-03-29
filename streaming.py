from flask import Flask, render_template, Response
import cv2


### connect with streaming.html to stream the video.

app = Flask(__name__) 
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success: # success is a bolean 
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/') # route page 
def index():
    return render_template('streaming.html')

@app.route('/video') # route page 
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__=='__main__':
    app.run(debug = True)