from flask import Flask, render_template, url_for, redirect, flash, request
from src.models import NewPatient, Patient
from src.forms import RegisterForm, PatientLoginForm
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
# -------------------------------------------------------------------- Admin Routes ------------------------------------------------------------------

@app.route('/admin')
def admin_dashboard():
    patients = Patient.query.all()
    newpatients = NewPatient.query.all()
    return render_template('admin_dashboard.html', patients=patients,newpatients=newpatients)

@app.route('/admin/approve_patient/<int:new_patient_id>', methods=['POST'])
def approve_patient(new_patient_id):
    new_patient = NewPatient.query.get(new_patient_id)
    if new_patient:
        patient_data = {
            'id': new_patient.id,
            'first_name': new_patient.first_name,
            'last_name': new_patient.last_name,
            'email': new_patient.email,
            'date_of_birth': new_patient.date_of_birth,
            'phone_number': new_patient.phone_number,
            'password': new_patient.password,
            'address': new_patient.address,
            'approved':new_patient.approved,
            # Add other fields here...
        }
        
        # Create a new entry in the Patient model
        patient = Patient(**patient_data)
        db.session.add(patient)
        db.session.commit()
        
        # Delete the entry from NewPatient
        db.session.delete(new_patient)
        db.session.commit()
        
        flash('Patient approved successfully.')
        # Notify patient about approval
        # Send email or notification to the patient
    return redirect('/admin')


@app.route('/admin/delete_patient/<int:new_patient_id>', methods=['POST'])
def delete_patient(new_patient_id):
    patient = NewPatient.query.get(new_patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
        flash('Patient deleted successfully.')
        # Notify patient about deletion if needed
    return redirect('/admin')

# -------------------------------------------------------------------- Doctor Routes -----------------------------------------------------------------
@app.route('/doctor_home')
def doctor_dashboard():
    patients = Patient.query.all()
    return render_template('doctor_dashboard.html', patients=patients)
# -------------------------------------------------------------------- Patient Routes ----------------------------------------------------------------
@app.route('/patient_register', methods=['GET', 'POST'])
def patient_register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_patient = NewPatient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            date_of_birth=form.date_of_birth.data,
            phone_number=form.phone_number.data,
            password=form.password.data,
            address=form.address.data,
        )
        db.session.add(new_patient)
        db.session.commit()

        flash('Your registration request has been sent to the Super Admin for approval.', category='success')
        return redirect(url_for('patient_register'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('patient_registration.html', form=form)


@app.route('/patient/login', methods=['GET', 'POST'])
def patient_login():
    form = PatientLoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Check if the provided credentials exist in the Patient model
        patient = Patient.query.filter_by(email=email, password=password).first()
        newpatient = NewPatient.query.filter_by(email=email, password=password).first()
        if newpatient:
            flash('Your registration is still pending approval.', category='warning')
        elif patient:
                # Allow access to the dashboard or wherever you redirect after login
            flash('Login successful!', category='success')
            return redirect('/doctor_home')
            # else:
            #     flash('Your registration is still pending approval.')
        else:
            flash('Invalid credentials. Please try again.',category='danger')

    return render_template('patient_login.html', form=form)



