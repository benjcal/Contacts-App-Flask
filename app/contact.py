from flask import Blueprint, request
from flask.json import jsonify
from .models import (contact_get,
                     contact_update,
                     contact_delete,
                     contact_new,
                     contact_get_all)

contact = Blueprint('contact', __name__)


# GET /contact/<id> -- get contact
@contact.route('/<id>', methods=['GET'])
def get(id):
    return jsonify(contact_get(id))


# PUT /contact/<id> -- update contact
@contact.route('/<id>', methods=['PUT', 'PATCH'])
def update(id):
    return jsonify(contact_update(id, request.get_json()))


# DELETE /contact/<id> -- get one contact
@contact.route('/<id>', methods=['DELETE'])
def delete(id):
    return jsonify(contact_delete(id))


# POST /contact -- create contact
@contact.route('', methods=['POST'])
def new():
    return jsonify(contact_new(request.get_json())), 201


# GET /contact -- get contacts
@contact.route('', methods=['GET'])
def get_contacts():
    return jsonify(contact_get_all())
