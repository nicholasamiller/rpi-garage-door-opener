import logging
import garage
from picamera import PiCamera
from flask import Flask, make_response, request, render_template, redirect, Response, send_file
import time
import io

app = Flask(__name__)
camera = PiCamera()

@app.route('/garage', methods=["POST"])
def toggleGarage():
    garage.triggerGarage()
    return redirect(request.referrer)

@app.route('/video_feed')
def video_feed():
     # Set camera resolution and frame rate
    camera.resolution = (640, 480)
    camera.rotation = 270
    camera.framerate = 30
    
     # Start camera preview
    camera.start_preview()
    time.sleep(2)  # Wait for camera to warm up

    def generate():
         while True:
             # Capture image from camera
             stream = io.BytesIO()
             camera.capture(stream, format='jpeg')
             stream.seek(0)
             yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/snapshot')
def snapshot():
    camera.resolution = (640, 480)
        # Capture a single image and store it in memory
    image = io.BytesIO()
    camera.capture(image, format='jpeg')
    camera.rotation=270
    # Reset the stream for reading
    image.seek(0)
        # Return the image as a response to the HTTP request
    return send_file(image, mimetype='image/jpeg')


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
