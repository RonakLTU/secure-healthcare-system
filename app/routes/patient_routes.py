from flask import request, render_template, redirect, session
from app.models.patient_model import create_patient_record, get_all_patients


def add_patient():

    if "role" not in session or session["role"] != "clinician":
        return "Access denied"

    if request.method == "POST":

        age = int(request.form.get("age"))

        if age < 1 or age > 120:
            return render_template("add_patient.html", error="Invalid age")

        patient_data = {

            "patient_id": request.form.get("patient_id"),
            "age": age,
            "sex": request.form.get("sex"),
            "blood_pressure": request.form.get("blood_pressure"),
            "cholesterol": request.form.get("cholesterol"),
            "fasting_blood_sugar": request.form.get("fasting_blood_sugar"),
            "resting_ecg": request.form.get("resting_ecg"),
            "exercise_angina": request.form.get("exercise_angina")

        }

        create_patient_record(patient_data)

        return redirect("/patients")

    return render_template("add_patient.html")


def view_patients():

    if "user_id" not in session:
        return redirect("/login")

    patients = get_all_patients()

    return render_template("patients.html", patients=patients)