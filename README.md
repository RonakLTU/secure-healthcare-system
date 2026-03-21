https://github.com/RonakLTU/secure-healthcare-system.git

**Secure Healthcare Management System**

The system simulates a real-world healthcare environment where:
•	Patients can register, login, view medical records, and book appointments
•	Clinicians can manage patient records and appointments
•	Admin can manage system users securely

Its focuses heavily on security, authentication, access control, and data protection

**Objectives**
•	Develop a secure web-based healthcare system
•	Apply SSDLC principles
•	Implement STRIDE threat modelling
•	Ensure secure coding practices
•	Demonstrate real-world role-based access

**Technologies Used**
Backend
•	Python (Flask Framework)
•	SQLite (User Authentication Database)
•	MongoDB (Patient & Appointment Records)
Frontend
•	HTML
•	CSS
•	JavaScript (Validation + UI interaction)
Security Libraries
•	Flask-Login (Authentication)
•	Flask-WTF (CSRF Protection)
•	Bcrypt (Password Hashing)
•	Cryptography
Testing
•	Pytest
Tools
•	VS Code
•	Git & GitHub
•	MongoDB Compass

**Security Features Implemented**
Authentication & Authorization
•	Secure login system using Flask-Login
•	Role-based access:
o	Patient
o	Clinician
o	Admin
Password Security
•	Password hashing using bcrypt
•	Strong password validation enforced
CSRF Protection
•	Implemented using Flask-WTF
Input Validation
•	Frontend (JavaScript)
•	Backend (Python validation)
Session Security
•	Secure session cookies
Logging System
•	Custom logging implemented
•	Tracks:
o	Login attempts
o	Registration
o	Patient record operations
o	Appointment booking
Logs stored locally:
logs/app.log (Logs excluded from GitHub for security)

**System Features**
Patient
•	Register & Login
•	View personal medical record
•	Book appointment
•	View appointment history
Clinician
•	Add patient records
•	Edit/Delete patient records
•	View all patient records
•	View patient appointments
Admin
•	Create clinician accounts
•	Manage users (delete)
•	View patient users

**Threat model created using STRIDE**
•	Spoofing → Fake login attempts
•	Tampering → Data modification
•	Repudiation → Lack of logs (fixed with logging)
•	Information Disclosure → Unauthorized access
•	Denial of Service → Input validation
•	Elevation of Privilege → Role-based access control
Trust boundaries implemented between:
•	User ↔ Web App
•	Web App ↔ Database

**Testing performed using Pytest:**
•	Authentication tests
•	Patient record tests
•	Security validation tests

**File Structure**
secure-healthcare-system/
│
├── app/
│ ├── models/
│ │ ├── user_model.py
│ │ ├── patient_model.py
│ │ └── auth_user.py
│ │
│ ├── routes/
│ │ ├── auth_routes.py
│ │ └── patient_routes.py
│ │
│ ├── security/
│ │ ├── password_utils.py
│ │ ├── csrf_protection.py
│ │ ├── login_manager.py
│ │ └── logger.py
│ │
│ ├── templates/
│ │ ├── base.html
│ │ ├── landing.html
│ │ ├── login.html
│ │ ├── register.html
│ │ │
│ │ ├── patient/
│ │ ├── clinician/
│ │ └── admin/
│ │
│ └── static/
│ ├── css/
│ ├── js/
│ └── img/
│
├── database/
│ └── auth.db
│
├── logs/
│ └── app.log
│
├── tests/
│ ├── test_auth.py
│ ├── test_patient.py
│ └── test_security.py
│
├── run.py
├── requirements.txt
├── .gitignore
└── README.md


**Diagram**

**System Architecture Diagram**

<img width="3285" height="2821" alt="1" src="https://github.com/user-attachments/assets/8a0d1997-f6ae-4cb7-a5d4-d0b30d29d248" />

**Trust Boundary Diagram**

<img width="3493" height="2925" alt="2" src="https://github.com/user-attachments/assets/cf305daf-7bb0-4244-afee-f43906a9f71f" />

**STRIDE Threat Model Diagram**

<img width="5147" height="3159" alt="3" src="https://github.com/user-attachments/assets/e2756ca2-5560-4a6d-b967-acfe800f3c52" />


**GDPR Considerations**
•	User data is securely stored and accessed
•	Passwords are encrypted (not stored in plain text)
•	Logs are not publicly exposed
•	Role-based access ensures data privacy

**Virtual environment**
Venv

**DECLARATION**

This assignment used generative artificial intelligence tools, including ChatGPT and Microsoft Copilot, to support the completion of this project.
AI tools were used for brainstorming, research, planning, feedback, editing.

In addition, diagramming and design tools such as Mermaid were used to create all diagrams, and for all visual assets (e.g., background vector images) were sourced from Freepik.

**REFERENCES**
OpenAI. (2025). ChatGPT [Large language model]. https://chat.openai.com/
Microsoft. (2025). Microsoft Copilot. https://copilot.microsoft.com/
Mermaid JS. (2025). Mermaid Diagramming Tool. https://mermaid.js.org/
Freepik Company. (2025). https://www.freepik.com/
