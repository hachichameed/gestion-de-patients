import streamlit as st
import requests

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

# Fonction pour supprimer un patient
def delete_patient(patient_id):
    response = requests.delete(f'https://hapi.fhir.org/baseR5/Patient/{patient_id}')
    return response.status_code

def app():
    st.title("Suppression d'un Patient")

    # Sélection du patient à supprimer
    patient_dict = get_patients_for_selection()
    if patient_dict:
        patient_name = st.selectbox("Sélectionnez un patient à supprimer", list(patient_dict.keys()))
        patient_id = patient_dict[patient_name]

        if st.button("Supprimer le patient"):
            status_code = delete_patient(patient_id)
            if status_code in [200, 204]:
                st.success("Patient supprimé avec succès.")
            else:
                st.error(f"Erreur lors de la suppression du patient (Code: {status_code})")
    else:
        st.write("Aucun patient à afficher.")

app()
