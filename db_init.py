from app import create_app
from app.models import db, new_contact

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()


contact_json = """\
{
    "first_name": "ben",
    "last_name": "cal",
    "date_of_birth": "1987-02-03",
    "addresses": ["some street", "another place"],
    "phones": ["12345", "67890"],
    "emails": ["b@c.co", "d@e.ep"]
}
"""

print(new_contact(contact_json).to_json())
