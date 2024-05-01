#!/usr/bin/python3
""" index file for the project """
from api.v1.views import app_views
from flask import jsonify, Flask, Blueprint
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ the ok status """
    ok = {"status": "OK"}
    return jsonify(ok)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ the stats count """
    counts = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(counts)


if __name__ == "__main__":
    pass
