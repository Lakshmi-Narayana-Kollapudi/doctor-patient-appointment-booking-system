from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired,ValidationError
from src.models import Patient
from src import db
from src import app

with app.app_context():
    db.create_all()

class RegisterForm(FlaskForm):
    def validate_email(self, email_to_check):
        email = Patient.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Please try a different email address')
        

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    date_of_birth = DateField(
        "Date of Birth",validators=[DataRequired()]
    )
    phone_number = StringField("Phone No", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters"),
            # Custom validator to ensure password contains letters and numbers
            lambda form, field: any(c.isalpha() for c in field.data)
            and any(c.isdigit() for c in field.data)
            or ("Password must contain letters and numbers"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    address = StringField("Address",validators=[DataRequired()])
    submit = SubmitField(label='Register')
