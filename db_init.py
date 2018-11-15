from app import create_app
from app.models import db, contact_new

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

# CSV Format: first_name,last_name,date_of_birth,email,address,phone
# files_names = ['MOCK_DATA_0.csv', 'MOCK_DATA_1.csv', 'MOCK_DATA_2.csv']
files_names = ['MOCK_DATA_small.csv']

for f in files_names:
    for line in open(f, encoding='utf8').readlines():
        line = line.strip()
        data = line.split(',')
        contact_new(
            dict(
                first_name=data[0],
                last_name=data[1],
                date_of_birth=data[2],
                emails=[{'email': data[3]}],
                addresses=[{'address': data[4]}],
                phones=[{'phone': data[5]}]
            )
        )
