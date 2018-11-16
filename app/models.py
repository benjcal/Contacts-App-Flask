from datetime import date
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# DB Models
#   -   Each class has a .to_dict() method which return
#       the data as a dictionary
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    # relationship in order to allow more than one entry
    addresses = db.relationship('Address', backref='person', lazy=True)
    emails = db.relationship('Email', backref='person', lazy=True)
    phones = db.relationship('Phone', backref='person', lazy=True)

    # convert class to dict to later serialize to json
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d'),
            'addresses': list(map(lambda e: e.to_dict(), self.addresses)),
            'emails': list(map(lambda e: e.to_dict(), self.emails)),
            'phones': list(map(lambda e: e.to_dict(), self.phones)),
        }


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(240), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'),
                           nullable=False)

    def to_dict(self):
        return {'id': self.id, 'address': self.address}


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'),
                           nullable=False)

    def to_dict(self):
        return {'id': self.id, 'email': self.email}


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(120), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'),
                           nullable=False)

    def to_dict(self):
        return {'id': self.id, 'phone': self.phone}


def _str_to_date(s):
    # takes a string in the format of YYYY-MM-DD and returns a python date.
    year = int(s.split('-')[0])
    month = int(s.split('-')[1])
    day = int(s.split('-')[2])

    return date(year, month, day)


def _validate_data(data):
    # make sure that the required fields are present as per the app specs
    if 'first_name' not in data:
        return {'ERROR': 'first_name is required'}

    if 'last_name' not in data:
        return {'ERROR': 'last_name is required'}

    if 'date_of_birth' not in data:
        return {'ERROR': 'date_of_birth is required'}

    if 'phones' not in data:
        return {'ERROR': 'phones is required'}

    if 'emails' not in data:
        return {'ERROR': 'emails is required'}

    else:
        return {}


def contact_get(id):
    c = Contact.query.get(id)
    if c is not None:
        return c.to_dict()
    else:
        return {}


def contact_update(id, data):
    c = Contact.query.get(id)

    if 'first_name' in data:
        c.first_name = data['first_name']

    if 'last_name' in data:
        c.last_name = data['last_name']

    if 'date_of_birth' in data:
        c.date_of_birth = _str_to_date(data['date_of_birth'])

    if 'addresses' in data:
        for i in data['addresses']:
            a = Address.query.get(i['id'])
            a.address = i['address']
            db.session.add(a)
            db.session.commit()

    if 'phones' in data:
        for i in data['phones']:
            p = Phone.query.get(i['id'])
            p.phone = i['phone']
            db.session.add(p)
            db.session.commit()

    if 'emails' in data:
        for i in data['emails']:
            e = Email.query.get(i['id'])
            e.email = i['email']
            db.session.add(e)
            db.session.commit()

    db.session.commit()
    return c.to_dict()


def contact_delete(id):
    c = Contact.query.get(id)
    if c is None:
        return {}

    for i in Address.query.filter_by(contact_id=id).all():
        db.session.delete(i)
        db.session.commit()

    for i in Email.query.filter_by(contact_id=id).all():
        db.session.delete(i)
        db.session.commit()

    for i in Phone.query.filter_by(contact_id=id).all():
        db.session.delete(i)
        db.session.commit()

    db.session.delete(Contact.query.get(id))
    db.session.commit()

    return {}


def contact_new(data):
    contact = Contact(
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=_str_to_date(data['date_of_birth'])
    )

    db.session.add(contact)
    db.session.commit()

    for e in data['addresses']:
        db.session.add(Address(contact_id=contact.id, address=e['address']))

    for e in data['emails']:
        db.session.add(Email(contact_id=contact.id, email=e['email']))

    for e in data['phones']:
        db.session.add(Phone(contact_id=contact.id, phone=e['phone']))

    db.session.commit()

    return contact.to_dict()


def contact_get_all():
    return list(map(lambda e: e.to_dict(), Contact.query.all()))
