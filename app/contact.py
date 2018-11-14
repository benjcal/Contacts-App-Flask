from flask import Blueprint, request
from flask.json import jsonify
from .models import db, Contact, gen_contact


contact = Blueprint('contact', __name__)


# GET /contact/<id> -- get one contact
@contact.route('/<id>', methods=['GET'])
def get_contact(id):
    return jsonify(Contact.query.get(id).to_dict())


# PUT /contact/<id> -- get one contact
@contact.route('/<id>', methods=['PUT'])
def update_contact(id):
    return jsonify(Contact.query.filter_by(id=id).first().to_dict())


# DELETE /contact/<id> -- get one contact
@contact.route('/<id>', methods=['DELETE'])
def delete_contact(id):
    c = Contact.query.filter_by(id=id).first()
    print(db.session.delete(c))
    db.session.commit()
    return jsonify(Contact.query.filter_by(id=id).first().to_dict())


# POST /contact -- create contact
@contact.route('', methods=['POST'])
def new_contcat():
    return jsonify(gen_contact(request.get_json()).to_dict()), 201


# GET /contact -- get contacts
@contact.route('', methods=['GET'])
def get_contacts():
    return jsonify(list(map(lambda e: e.to_dict(), Contact.query.all())))
