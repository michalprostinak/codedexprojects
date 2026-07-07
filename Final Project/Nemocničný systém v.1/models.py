"""
Hospital Management System – Doctor a Patient triedy
"""


class Doctor:
    def __init__(self, name, password, specialization):
        self.name = name
        self.password = password
        self.specialization = specialization
        self.patients = []  # zoznam Patient objektov priradených tomuto lekárovi

    def add_patient(self, patient):
        self.patients.append(patient)
        patient.doctor_name = self.name
        patient.department = self.specialization

    def view_patients(self):
        if not self.patients:
            print(f"\nDr. {self.name} nemá zatiaľ žiadnych pacientov.")
            return
        print(f"\n👨‍⚕️ Pacienti Dr. {self.name} ({self.specialization}):")
        for i, p in enumerate(self.patients, start=1):
            print(f"{i}. {p.name} ({p.age}) – {p.diagnosis} [Status: {p.status}]")

    def find_patient_by_name(self, name):
        for p in self.patients:
            if p.name.lower() == name.lower():
                return p
        return None

    def remove_patient(self, patient):
        if patient in self.patients:
            self.patients.remove(patient)


class Patient:
    # jednoduché počítadlo pre unikátne ID pacienta (napr. pre PDF názvy súborov)
    _next_id = 1

    def __init__(self, name, age, diagnosis, department=None, doctor_name=None):
        self.id = Patient._next_id
        Patient._next_id += 1

        self.name = name
        self.age = age
        self.diagnosis = diagnosis
        self.department = department
        self.doctor_name = doctor_name
        self.treatment = "Not yet determined"
        self.notes = ""
        self.status = "Hospitalized"  # Hospitalized / Emergency / Recovered / Discharged
        self.added_by = doctor_name  # kto pacienta pridal

    def update_treatment(self, treatment):
        self.treatment = treatment

    def update_notes(self, notes):
        self.notes = notes

    def update_status(self, status):
        self.status = status

    def discharge(self):
        self.status = "Discharged"

    def __str__(self):
        return f"{self.name} ({self.age}) – {self.diagnosis} [{self.status}]"
