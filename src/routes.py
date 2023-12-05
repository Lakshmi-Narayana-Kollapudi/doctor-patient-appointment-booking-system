from flask import Flask, render_template, url_for, redirect, flash
from src.models import Patient
from src.forms import RegisterForm
from src import app
from src import db

# Simulating a super admin's email for demonstration
super_admin_email = 'superadmin@example.com'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def registration():
    return render_template('registration.html')

@app.route('/patientregister', methods=['GET', 'POST'])
def patient_register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            date_of_birth=form.date_of_birth.data,
            phone_number=form.phone_number.data,
            password=form.password.data,
            address=form.address.data
        )
        db.session.add(new_patient)
        db.session.commit()

        flash('Registration request sent for approval!', category='success')
        return redirect(url_for('patient_register'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('patient_registration.html', form=form)


