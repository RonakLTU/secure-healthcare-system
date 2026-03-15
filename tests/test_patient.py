from app.models.patient_model import create_patient_record, get_all_patients


def test_insert_patient():

    patient = {

        "patient_id": "TEST100",
        "age": 30,
        "sex": "Male",
        "blood_pressure": "120",
        "cholesterol": "200",
        "fasting_blood_sugar": "No",
        "resting_ecg": "Normal",
        "exercise_angina": "No"
    }

    record_id = create_patient_record(patient)

    assert record_id is not None


def test_get_patients():

    patients = get_all_patients()

    assert isinstance(patients, list)