"""
Prihlasovanie lekárov do systému.
"""
from doctors_db import doctors


def login():
    print("\n🏥 Hospital System – Login")
    print("=" * 30)

    attempts = 3
    while attempts > 0:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        for doctor in doctors:
            if doctor.name.lower() == username.lower() and doctor.password == password:
                print(f"\n✅ Welcome Dr. {doctor.name}")
                print(f"Specialization: {doctor.specialization}\n")
                return doctor

        attempts -= 1
        print(f"❌ Nesprávne meno alebo heslo. Ostávajúce pokusy: {attempts}")

    print("\n🚫 Príliš veľa neúspešných pokusov. Program sa ukončí.")
    return None
