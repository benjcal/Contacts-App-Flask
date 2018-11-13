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
        return {'first_name': self.first_name,
                'addresses': self.addresses}


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(240), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('contact.id'),
                          nullable=False)

    # convert to list
    def to_list(self):
        return [self.id, self.address]


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('contact.id'),
                          nullable=False)


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('contact.id'),
                          nullable=False)
