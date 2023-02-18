import logging
import garage
import atexit
from flask import Flask, make_response, request, render_template, redirect


app = Flask(__name__)

@app.route('/garage', methods=["POST"])
def toggleGarage():
    garage.triggerGarage()
    return redirect(request.referrer)


def cleanup():
    logging.info("Cleaning up...")
    # Stop the Flask server
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    atexit.register(cleanup)
    app.run(host='0.0.0.0', port=5000,debug=True)
