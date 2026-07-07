"""
Databáza lekárov a mapovanie diagnóz na špecializácie.
"""
from models import Doctor

# Zoznam všetkých lekárov v systéme
doctors = [
    Doctor("Prostinak", "1234", "Cardiology"),
    Doctor("Kovac", "5678", "Neurology"),
    Doctor("Horvathova", "1111", "Orthopedics"),
    Doctor("Bielik", "2222", "General Medicine"),
]

# Mapovanie: kľúčové slovo v diagnóze -> špecializácia
# (hľadá sa, či sa kľúčové slovo nachádza v texte diagnózy, takže to funguje
#  aj pre "Severe heart disease" alebo "Chronic heart disease")
DIAGNOSIS_TO_SPECIALIZATION = {
    "heart": "Cardiology",
    "arrhythmia": "Cardiology",
    "blood pressure": "Cardiology",
    "migraine": "Neurology",
    "seizure": "Neurology",
    "stroke": "Neurology",
    "fracture": "Orthopedics",
    "broken": "Orthopedics",
    "bone": "Orthopedics",
    "flu": "General Medicine",
    "fever": "General Medicine",
    "cold": "General Medicine",
    "Coronary artery diseases": "Cardiology"
}

DEFAULT_SPECIALIZATION = "General Medicine"


def get_specialization_for_diagnosis(diagnosis):
    """Nájde vhodnú špecializáciu na základe textu diagnózy."""
    diagnosis_lower = diagnosis.lower()
    for keyword, specialization in DIAGNOSIS_TO_SPECIALIZATION.items():
        if keyword in diagnosis_lower:
            return specialization
    return DEFAULT_SPECIALIZATION


def find_doctor_for_specialization(specialization):
    """
    Nájde lekára danej špecializácie s najmenším počtom pacientov
    (rovnomerné rozloženie záťaže medzi lekárov rovnakého odboru).
    """
    matching_doctors = [d for d in doctors if d.specialization == specialization]

    if not matching_doctors:
        # ak neexistuje lekár danej špecializácie, vezmeme General Medicine
        matching_doctors = [d for d in doctors if d.specialization == DEFAULT_SPECIALIZATION]

    if not matching_doctors:
        return None

    # lekár s najmenej pacientmi dostane nového pacienta
    return min(matching_doctors, key=lambda d: len(d.patients))


def find_doctor_by_name(name):
    for d in doctors:
        if d.name.lower() == name.lower():
            return d
    return None
