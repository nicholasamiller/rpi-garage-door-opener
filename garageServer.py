import logging
import garage
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from flask import Flask, make_response, request, render_template, redirect, Response, send_file
from flask_socketio import SocketIO
from picamera2.outputs import FileOutput


import time
import io

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/garage', methods=["POST"])
def toggleGarage():
    garage.triggerGarage()
    return redirect(request.referrer)

def generate_frames():
    with Picamera2() as picam2:
        picam2.configure(picam2.create_video_configuration())
        encoder = H264Encoder()
        
        buffer = io.Bytes()
        output = FileOutput(buffer)
        picam2.start_recording(encoder, output)
        
        while True:
            try:
                # Wait for the next frame
                output.wait_for_frame()

                # Get the latest frame from the output object
                frame = output.get_frame()

                # Create a bytes buffer to hold the frame data
                frameBuffer = io.BytesIO()

                # Save the frame data in the buffer in JPEG format
                frame.save(frameBuffer, format='jpeg')

                # Convert the buffer contents to a bytes object and yield it to the client
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frameBuffer.getvalue() + b'\r\n')
                
            except KeyboardInterrupt:
                # Stop recording and exit
                picam2.stop_recording()
                break

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


    


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
