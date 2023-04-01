import logging
import garage
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from flask import Flask, make_response, request, render_template, redirect, Response, send_file
from picamera2.outputs import FileOutput
from libcamera import Transform
import numpy as np
from PIL import Image



import time
import io

app = Flask(__name__)


@app.route('/garage', methods=["POST"])
def toggleGarage():
    garage.triggerGarage()
    return redirect(request.referrer)

@app.route('/capture',methods=["GET"])
def capture():
    with Picamera2() as picam2:
        buffer = io.BytesIO()
        still_config = picam2.create_still_configuration(transform=Transform())
        picam2.configure(still_config)
        picam2.start()
        time.sleep(1)
        
        array = picam2.capture_array("main")
        rot_array=np.rot90(array)
        img = Image.fromarray(rot_array)
        img.save(buffer, format='JPEG')

        buffer.seek(0)
        return Response(buffer,mimetype='image/jpeg')


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
