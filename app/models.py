from datetime import date
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


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
            'id': self.id, 'first_name': self.first_name,
            'last_name': self.last_name,
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
    # takes a string in the format of YYYY-MM-DD and returns a date
    year = int(s.split('-')[0])
    month = int(s.split('-')[1])
    day = int(s.split('-')[2])

    return date(year, month, day)


def gen_contact(res_dict):

    contact = Contact(
        first_name=res_dict['first_name'],
        last_name=res_dict['last_name'],
        date_of_birth=_str_to_date(res_dict['date_of_birth'])
    )

    db.session.add(contact)
    db.session.commit()

    for e in res_dict['addresses']:
        db.session.add(Address(contact_id=contact.id, address=e))

    for e in res_dict['emails']:
        db.session.add(Email(contact_id=contact.id, email=e))

    for e in res_dict['phones']:
        db.session.add(Phone(contact_id=contact.id, phone=e))

    db.session.commit()

    return contact
