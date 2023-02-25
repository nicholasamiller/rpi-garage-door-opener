import logging
import garage
from picamera import PiCamera
from flask import Flask, make_response, request, render_template, redirect, Response, send_file
import time
import io

app = Flask(__name__)

@app.route('/garage', methods=["POST"])
def toggleGarage():
    garage.triggerGarage()
    return redirect(request.referrer)

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
