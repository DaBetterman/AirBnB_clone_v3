#!/usr/bin/python3
""" view for State objects that handles all default RESTFul API actions """


from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route('/states', strict_slashes=False)
def states():
    """ return states """
    states = storage.all(State).values()
    lst = [i.to_dict() for i in states]
    return jsonify(lst)


@app_views.route('/states/<string:s_id>', strict_slashes=False)
def states_id(s_id):
    """ return a state using id """
    s = storage.get("State", s_id)
    if s:
        return jsonify(s.to_dict())
    abort(404)


@app_views.route('/states/<string:s_id>', methods=['DELETE'], strict_slashes=False)
def state_delete(s_id):
    """ deletes a state """
    s = storage.get("State", s_id)
    if s:
        s.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_states():
    """ posting a state """
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    s = State(**request.get_json())
    storage.save()
    return make_response(jsonify(s.to_dict()), 201)


@app_views.route('/states/<string:s_id>', methods=['PUT'], strict_slashes=False)
def state_put(s_id):
    """ put to update a state """
    s = storage.get("State", s_id)
    if not s:
        abort(404)
        if not request.get_json():
            return make_responde(jsonify({'error': 'Not a JSON'}), 400)
        for k, v in request.get_json().items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(s, k, v)
    s.save()
    return jsonify(s.to_dict())
