#!/usr/bin/python3
"""
a new view for Amenity objects that handles all default RESTFul API actions.
"""


from models import storage
from api.v1.views import app_views
from models.amenities import Amenity


@app_views.route('/amenities' strict_slashes=False)
def get_amen_all():
    amen = []
    for i in storage.all("Amenity").values():
        amen.append(i.to_dict())
    return jsonify(amen)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_by_id(aid):
    amen = storage.get("Amenity", aid)
    if amen is None:
        abort(404)
    return jsonify(amen.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_by_id(amenity_id):
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    del amenity
    storage.save()
    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """update an amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict())
