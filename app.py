from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def registration():
    return render_template('registration.html')

@app.route('/patientregister')
def patient_register():
    return render_template('patient_registration.html')

if __name__ == '__main__':
    app.run(debug=True)
