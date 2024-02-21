import streamlit as st
import requests
from datetime import datetime

st.set_page_config(layout="wide")

# Fonction pour obtenir la liste des patients pour la sélection
def get_patients_for_selection():
    response = requests.get('https://hapi.fhir.org/baseR5/Patient?_sort=-_lastUpdated')
    if response.status_code == 200:
        data = response.json()
        if 'entry' in data:
            patient_list = {}
            for patient_entry in data['entry']:
                patient = patient_entry['resource']
                patient_id = patient['id']
                names = patient.get('name', [{}])
                first_name = names[0].get('given', [""])[0] if names else ""
                last_name = names[0].get('family', "") if names else ""
                full_name = f"{first_name} {last_name}".strip()
                display_name = f"{full_name}, ID: {patient_id}" if full_name else f"ID: {patient_id}"
                patient_list[display_name] = patient_id
            return patient_list
    return {}

# Fonction pour obtenir les détails d'un patient spécifique
def get_patient_details(patient_id):
    response = requests.get(f'https://hapi.fhir.org/baseR5/Patient/{patient_id}')
    if response.status_code == 200:
        return response.json()
    return None

# Fonction pour mettre à jour les données d'un patient
def update_patient(patient_id, data):
    response = requests.put(f'https://hapi.fhir.org/baseR5/Patient/{patient_id}', json=data)
    return response.status_code

def edit_patient_page():
    st.title("Modification d'un Patient")

    patient_dict = get_patients_for_selection()
    if patient_dict:
        selected_patient = st.selectbox("Sélectionnez un patient à modifier", list(patient_dict.keys()))
        patient_id = patient_dict[selected_patient]

        patient_data = get_patient_details(patient_id)
        if patient_data:
            with st.form(key='update_patient_form'):
                first_name = st.text_input("Prénom", value=patient_data.get('name', [{}])[0].get('given', [""])[0])
                last_name = st.text_input("Nom de famille", value=patient_data.get('name', [{}])[0].get('family', ""))
                birth_date_str = patient_data.get('birthDate', "")
                birth_date = st.date_input("Date de naissance", value=datetime.strptime(birth_date_str, '%Y-%m-%d') if birth_date_str else datetime.today())
                gender = st.selectbox("Genre", options=["male", "female", "other", "unknown"], index=["male", "female", "other", "unknown"].index(patient_data.get('gender', "unknown")))
                address = st.text_area("Adresse", value=patient_data.get('address', [{}])[0].get('text', ""))

                submit_button = st.form_submit_button("Mettre à jour le patient")
                if submit_button:
                    updated_data = {
                        "resourceType": "Patient",
                        "id": patient_id,
                        "name": [{"given": [first_name], "family": last_name}],
                        "gender": gender,
                        "birthDate": str(birth_date),
                        "address": [{"text": address}]
                    }

                    status_code = update_patient(patient_id, updated_data)
                    if status_code == 200:
                        st.success("Patient mis à jour avec succès.")
                    else:
                        st.error(f"Erreur lors de la mise à jour du patient (Code: {status_code})")
    else:
        st.write("Aucun patient à afficher.")


edit_patient_page()