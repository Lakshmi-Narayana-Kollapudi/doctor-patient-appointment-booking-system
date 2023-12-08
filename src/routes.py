from flask import Flask, render_template, url_for, redirect, flash, session, request
from src.models import NewPatient, Patient, NewDoctor, Doctor
from src.forms import RegisterForm, PatientLoginForm, DoctorRegisterForm, DoctorLoginForm
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
    doctors = Doctor.query.all()
    newdoctors = NewDoctor.query.all()
    return render_template('/admin/admin_dashboard.html', patients=patients,newpatients=newpatients,doctors=doctors,newdoctors=newdoctors)

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
        }
        
        # Create a new entry in the Patient model
        patient = Patient(**patient_data)
        db.session.add(patient)
        db.session.commit()
        
        # Delete the entry from NewPatient
        db.session.delete(new_patient)
        db.session.commit()
        
        flash('Patient approved successfully.')

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


@app.route('/admin/approve_doctor/<int:new_doctor_id>', methods=['POST'])
def approve_doctor(new_doctor_id):
    new_doctor = NewDoctor.query.get(new_doctor_id)
    if new_doctor:
        doctor_data = {
            'id': new_doctor.id,
            'first_name': new_doctor.first_name,
            'last_name': new_doctor.last_name,
            'doctor_id': new_doctor.doctor_id,
            'speciality': new_doctor.speciality,
            'email': new_doctor.email,
            'date_of_birth': new_doctor.date_of_birth,
            'phone_number': new_doctor.phone_number,
            'password': new_doctor.password,
            'address': new_doctor.address,
            # Add other fields here...
        }
        
        # Create a new entry in the Patient model
        doctor = Doctor(**doctor_data)
        db.session.add(doctor)
        db.session.commit()
        
        # Delete the entry from NewPatient
        db.session.delete(new_doctor)
        db.session.commit()
        
        flash('Doctor approved successfully.')
    return redirect('/admin')

@app.route('/admin/delete_doctor/<int:new_doctor_id>', methods=['POST'])
def delete_doctor(new_doctor_id):
    doctor = NewDoctor.query.get(new_doctor_id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        flash('Doctor deleted successfully.')

    return redirect('/admin')
# -------------------------------------------------------------------- Doctor Routes -----------------------------------------------------------------
@app.route('/doctor/dashboard')
def doctor_dashboard():
    patients = Patient.query.all()
    doctor_id = session.get('doctor_id')
    if doctor_id:
        # Fetch patient's specific data from the database using patient_id
        doctor = Doctor.query.get(doctor_id)

        if doctor:
            # Pass patient data to the dashboard template
            return render_template('/doctor/doctor_dashboard.html', doctor=doctor,patients=patients)
        else:
            flash('Doctor data not found.')
            return redirect('/doctor/login')
    else:
        flash('Please log in first.')
        return redirect('/doctor/login')


@app.route('/doctor/register', methods=['GET', 'POST'])
def doctor_register():
    form = DoctorRegisterForm()
    if form.validate_on_submit():
        new_doctor = NewDoctor(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            doctor_id=form.doctor_id.data,
            speciality=form.speciality.data,
            email=form.email.data,
            date_of_birth=form.date_of_birth.data,
            phone_number=form.phone_number.data,
            password=form.password.data,
            address=form.address.data,
        )
        db.session.add(new_doctor)
        db.session.commit()

        flash('Your registration request has been sent to the Super Admin for approval.', category='success')
        return redirect(url_for('doctor_register'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('/doctor/doctor_registration.html', form=form)


@app.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    form = DoctorLoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Check if the provided credentials exist in the Patient model
        doctor = Doctor.query.filter_by(email=email, password=password).first()
        newdoctor = NewDoctor.query.filter_by(email=email, password=password).first()
        if newdoctor:
            flash('Your registration is still pending approval.', category='warning')
        elif doctor:
            # Allow access to the dashboard or wherever you redirect after login
            flash('Login successful!', category='success')
            session['doctor_id'] = doctor.id
            return redirect('/doctor/dashboard')
            # else:
            #     flash('Your registration is still pending approval.')
        else:
            flash('Invalid credentials. Please try again.',category='danger')

    return render_template('/doctor/doctor_login.html', form=form)
# -------------------------------------------------------------------- Patient Routes ----------------------------------------------------------------
@app.route('/patient/dashboard')
def patient_dashboard():
    doctors=Doctor.query.all()
    patient_id = session.get('patient_id')
    if patient_id:
        # Fetch patient's specific data from the database using patient_id
        patient = Patient.query.get(patient_id)

        if patient:
            # Pass patient data to the dashboard template
            return render_template('/patient/patient_dashboard.html', patient=patient,doctors=doctors)
        else:
            flash('Patient data not found.')
            return redirect('/patient/login')
    else:
        flash('Please log in first.')
        return redirect('/patient/login')



@app.route('/patient/register', methods=['GET', 'POST'])
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

    return render_template('/patient/patient_registration.html', form=form)


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
            session['patient_id'] = patient.id
            return redirect('/patient/dashboard')
            # else:
            #     flash('Your registration is still pending approval.')
        else:
            flash('Invalid credentials. Please try again.',category='danger')

    return render_template('/patient/patient_login.html', form=form)



