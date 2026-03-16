import sqlite3
from flask import request, render_template, redirect
from flask_login import current_user

from app.models.patient_model import create_patient_record, get_all_patients

DATABASE = "database/auth.db"


# ==============================
# ADD PATIENT RECORD
# ==============================

def add_patient():

    # Only clinicians allowed
    if current_user.role != "clinician":
        return redirect("/")

    if request.method == "POST":

        patient_data = {

            "patient_email": request.form.get("patient_email"),
            "age": request.form.get("age"),
            "sex": request.form.get("sex"),
            "blood_pressure": request.form.get("blood_pressure"),
            "cholesterol": request.form.get("cholesterol"),
            "fasting_blood_sugar": request.form.get("fasting_blood_sugar"),
            "resting_ecg": request.form.get("resting_ecg"),
            "exercise_angina": request.form.get("exercise_angina")

        }

        create_patient_record(patient_data)

        return redirect("/patients")

    # GET request → load patient list for dropdown

    with sqlite3.connect(DATABASE) as conn:

        cursor = conn.cursor()

        cursor.execute(
            "SELECT name,email FROM users WHERE role='patient'"
        )

        patients = cursor.fetchall()

    patient_list = []

    for p in patients:

        patient_list.append({
            "name": p[0],
            "email": p[1]
        })

    return render_template(
        "add_patient.html",
        patients=patient_list
    )


# ==============================
# VIEW ALL PATIENT RECORDS
# ==============================

def view_patients():

    # Only clinicians allowed
    if current_user.role != "clinician":
        return redirect("/")

    patients = get_all_patients()

    return render_template(
        "patients.html",
        patients=patients
    )
