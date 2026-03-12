from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create database
db = client["secure_healthcare_db"]

# Create collection
patients_collection = db["patients"]


def create_patient_record(data):

    result = patients_collection.insert_one(data)

    return result.inserted_id


def get_all_patients():

    patients = list(patients_collection.find())

    return patients