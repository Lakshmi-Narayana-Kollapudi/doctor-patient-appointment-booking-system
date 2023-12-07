from src import db


class NewPatient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    approved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Item {self.email}"
    
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    approved = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Item {self.email}"
