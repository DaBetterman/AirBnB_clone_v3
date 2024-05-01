#!/usr/bin/python3
"""  endpoint (route) will be to return the status of the API """

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint, make_response
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """ handling execption """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ handling not found """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    the_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    the_port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=the_host, port=the_port, threaded=True, debug=True)
