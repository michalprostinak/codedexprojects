"""
🏥 Hospital Management System 2.0
Hlavný program – spája prihlasovanie, pacientov, automatické
prideľovanie lekárov, liečbu a PDF prepúšťaciu správu.
"""
from models import Patient
from doctors_db import (
    doctors,
    get_specialization_for_diagnosis,
    find_doctor_for_specialization,
)
from login import login
from pdf_reports import generate_discharge_report


def print_menu(current_doctor):
    print("\n🏥 Hospital Management System")
    print(f"(Logged in as: Dr. {current_doctor.name} – {current_doctor.specialization})")
    print("1. Add patient")
    print("2. View my patients")
    print("3. Update treatment / notes")
    print("4. Discharge patient (generate PDF)")
    print("5. View all patients (sorted by department)")
    print("6. Search patient")
    print("7. Logout")
    print("8. Exit program")


def add_patient(current_doctor):
    print("\n➕ New Patient Registration")
    name = input("Patient name: ").strip()
    age = input("Age: ").strip()
    diagnosis = input("Diagnosis: ").strip()

    if not name or not diagnosis:
        print("⚠️ Patient name and diagnosis are required.")
        return

    try:
        age = int(age)
    except ValueError:
        print("⚠️ Age must be a number.")
        return

    # automatické určenie špecializácie podľa diagnózy
    specialization = get_specialization_for_diagnosis(diagnosis)
    assigned_doctor = find_doctor_for_specialization(specialization)

    if assigned_doctor is None:
        print("⚠️ There is no doctor available to whom the patient can be assigned.")
        return

    patient = Patient(name=name, age=age, diagnosis=diagnosis)
    patient.added_by = current_doctor.name  # kto pacienta zaevidoval
    assigned_doctor.add_patient(patient)

    print("\n✅ Pacient bol pridaný a automaticky priradený:")
    print(f"   Oddelenie: {specialization}")
    print(f"   Priradený lekár: Dr. {assigned_doctor.name}")
    print(f"   Zaevidoval: Dr. {current_doctor.name}")


def view_my_patients(current_doctor):
    current_doctor.view_patients()


def update_treatment(current_doctor):
    if not current_doctor.patients:
        print("\nNemáte žiadnych pacientov.")
        return

    view_my_patients(current_doctor)
    name = input("\nMeno pacienta, ktorému chcete upraviť liečbu: ").strip()
    patient = current_doctor.find_patient_by_name(name)

    if patient is None:
        print("⚠️ Pacient sa nenašiel medzi vašimi pacientmi.")
        return

    print(f"\nAktuálna liečba: {patient.treatment}")
    new_treatment = input("Nová liečba (Enter = nezmeniť): ").strip()
    if new_treatment:
        patient.update_treatment(new_treatment)

    print(f"Aktuálne poznámky: {patient.notes or '-'}")
    new_notes = input("Nové poznámky (Enter = nezmeniť): ").strip()
    if new_notes:
        patient.update_notes(new_notes)

    print("\n✅ Údaje pacienta boli aktualizované.")


def discharge_patient(current_doctor):
    if not current_doctor.patients:
        print("\nNemáte žiadnych pacientov.")
        return

    view_my_patients(current_doctor)
    name = input("\nMeno pacienta na prepustenie: ").strip()
    patient = current_doctor.find_patient_by_name(name)

    if patient is None:
        print("⚠️ Pacient sa nenašiel medzi vašimi pacientmi.")
        return

    patient.discharge()
    filepath = generate_discharge_report(patient)

    print("\n🖨️ Prepúšťacia správa bola vytvorená:")
    print(f"   📄 {filepath}")
    print(f"   Status pacienta: {patient.status}")


def view_all_patients_sorted():
    print("\n📋 Zoznam všetkých pacientov podľa oddelenia:")

    # zoskupíme podľa oddelenia
    departments = {}
    for doctor in doctors:
        for patient in doctor.patients:
            departments.setdefault(patient.department, []).append(patient)

    if not departments:
        print("Žiadni pacienti v systéme.")
        return

    for department in sorted(departments.keys()):
        print(f"\n{department.upper()}")
        print("-" * len(department))
        for i, patient in enumerate(departments[department], start=1):
            print(f"{i}. {patient.name} – {patient.diagnosis} "
                  f"(Dr. {patient.doctor_name}, status: {patient.status})")


def search_patient():
    name = input("\n🔍 Meno pacienta, ktorého hľadáte: ").strip().lower()
    found = []
    for doctor in doctors:
        for patient in doctor.patients:
            if name in patient.name.lower():
                found.append(patient)

    if not found:
        print("Pacient sa nenašiel.")
        return

    print(f"\nNájdených {len(found)} pacient(ov):")
    for patient in found:
        print(f"- {patient.name} ({patient.age}) – {patient.diagnosis}")
        print(f"  Oddelenie: {patient.department}, Lekár: Dr. {patient.doctor_name}, "
              f"Status: {patient.status}")


def doctor_session(current_doctor):
    """Menu pre konkrétneho prihláseného lekára. Vráti True ak chce ukončiť celý program."""
    while True:
        print_menu(current_doctor)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_patient(current_doctor)
        elif choice == "2":
            view_my_patients(current_doctor)
        elif choice == "3":
            update_treatment(current_doctor)
        elif choice == "4":
            discharge_patient(current_doctor)
        elif choice == "5":
            view_all_patients_sorted()
        elif choice == "6":
            search_patient()
        elif choice == "7":
            print(f"\n👋 Dr. {current_doctor.name} sa odhlásil.")
            return False
        elif choice == "8":
            print("\nGoodbye!")
            return True
        else:
            print("⚠️ Neplatná voľba, skús znova.")


def main():
    while True:
        current_doctor = login()
        if current_doctor is None:
            break  # priveľa zlých pokusov o prihlásenie

        should_exit = doctor_session(current_doctor)
        if should_exit:
            break


if __name__ == "__main__":
    main()
