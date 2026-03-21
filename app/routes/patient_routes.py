import sqlite3
from flask import request, render_template, redirect
from flask_login import current_user

from app.models.patient_model import create_patient_record, patients_collection
from app.security.logger import log_event

DATABASE = "database/auth.db"


# ==============================
# ADD PATIENT
# ==============================
def add_patient():

    if current_user.role != "clinician":
        return redirect("/")

    if request.method == "POST":

        patient_id = str(request.form.get("patient_id"))

        patient_data = {
            "patient_id": patient_id,
            "name": request.form.get("name"),
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

        log_event(f"Patient record added: {patient_id} by {current_user.email}")

        return redirect("/clinician_dashboard?success=Patient record added successfully")

    # GET → dropdown
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name,email FROM users WHERE role='patient'")
        patients = cursor.fetchall()

    patient_list = [{"name": p[0], "email": p[1]} for p in patients]

    return render_template("add_patient.html", patients=patient_list)


# ==============================
# VIEW PATIENTS
# ==============================
def view_patients():

    search_query = request.args.get("search")

    if search_query:
        patients = list(patients_collection.find({
            "$or": [
                {"patient_id": str(search_query)},
                {"patient_email": search_query}
            ]
        }))
    else:
        patients = list(patients_collection.find())

    return render_template("patients.html", patients=patients)


# ==============================
# EDIT PATIENT
# ==============================
def edit_patient(patient_id):

    if current_user.role != "clinician":
        return redirect("/")

    patient = patients_collection.find_one({
        "patient_id": str(patient_id)
    })

    if request.method == "POST":

        updated_data = {
            "patient_id": str(request.form.get("patient_id")),
            "name": request.form.get("name"),
            "patient_email": request.form.get("patient_email"),
            "age": request.form.get("age"),
            "sex": request.form.get("sex"),
            "blood_pressure": request.form.get("blood_pressure"),
            "cholesterol": request.form.get("cholesterol"),
            "fasting_blood_sugar": request.form.get("fasting_blood_sugar"),
            "resting_ecg": request.form.get("resting_ecg"),
            "exercise_angina": request.form.get("exercise_angina")
        }

        patients_collection.update_one(
            {"patient_id": str(patient_id)},
            {"$set": updated_data}
        )

        log_event(f"Patient record updated: {patient_id}")

        return redirect("/patients?success=Record updated successfully")

    # dropdown
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name,email FROM users WHERE role='patient'")
        patients = cursor.fetchall()

    patient_list = [{"name": p[0], "email": p[1]} for p in patients]

    return render_template("add_patient.html", patient=patient, patients=patient_list)


# ==============================
# DELETE PATIENT
# ==============================
def delete_patient(patient_id):

    if current_user.role != "clinician":
        return redirect("/")

    patients_collection.delete_one({
        "patient_id": str(patient_id)
    })

    log_event(f"Patient record deleted: {patient_id}")

    return redirect("/patients?success=Record deleted successfully")

