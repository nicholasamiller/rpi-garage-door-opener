import logging
import garage
import atexit
from flask import Flask, make_response, request

app = Flask(__name__)


@app.route('/garage')
def garage():
    garage.triggerGarage()
    response = make_response('OK')
    response.status_code = 200
    return response


def cleanup():
    logging.info("Cleaning up...")
    # Stop the Flask server
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()



if __name__ == '__main__':
    atexit.register(cleanup)
    app.run(host='0.0.0.0', port=5000,debug=True)