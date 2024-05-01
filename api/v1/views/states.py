#!/usr/bin/python3
""" view for State objects that handles all default RESTFul API actions """


from models import storage
from models.state import State
from . import app_views
from flask import jsonify


@app_views.route('/states', strict_slashes=False)
def states():
    """ return states """
    states = storage.all(State).values()
    lst = [i.to_dict() for i in states]
    return jsonify(lst)


@app_views.route('/states/<int:state_id>', strict_slashes=False)
def states_id(state_id):
    """ return a state using id """
    from api.v1.app import not_found
    states = storage.all(State).values()
    lst = [i.to_dict() for i in states]
    try:
        state = lst[state_id]
        return jsonify(state)
    except IndexError as e:
        not_found(e)
