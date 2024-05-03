#!/usr/bin/python3
""" a new view for City objects that handles all default RESTFul API actions """


from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import Flask, make_response, abort, jsonify


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False)
def get_cities(sid):
    """ return cities """
    states = storage.get('State', sid)
    if states is None:
        abort(404)
    lst = []
    for i in states.cities:
        lst.append(i.to_dict())
    return jsonify(lst)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(cid):
    city = storage.get("City", cid)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(cid):
    city = storage.get('City', cid)
    if city is None:
        abort(404)
    del city
    storage.save()
    return make_response(jsonify({}), 200)


def post_city(sid):
    """create a new city"""
    state = storage.get("State", sid)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs = request.get_json()
    kwargs['state_id'] = sid
    city = City(**kwargs)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(cid):
    """update a city"""
    city = storage.get("City", cid)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, v in request.get_json().items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict())
