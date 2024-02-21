import streamlit as st
import requests
import json

st.set_page_config(layout="wide")

def create_patient(data):
    response = requests.post('https://hapi.fhir.org/baseR5/Patient', json=data)
    return response.status_code

def app():
    st.title("Ajouter un nouveau patient")

    with st.form("patient_form"):
        first_name = st.text_input("Prénom")
        last_name = st.text_input("Nom de famille")
        birth_date = st.date_input("Date de naissance")
        gender = st.selectbox("Genre", options=["male", "female", "other", "unknown"])
        address = st.text_area("Adresse")

        submit_button = st.form_submit_button("Créer le patient")

        if submit_button:
            patient_data = {
                "resourceType": "Patient",
                "name": [{"given": [first_name], "family": last_name}],
                "gender": gender,
                "birthDate": str(birth_date),
                "address": [{"text": address}]
            }

            status_code = create_patient(patient_data)
            if status_code == 201:
                st.success("Patient ajouté avec succès!")
            else:
                st.error(f"Erreur lors de l'ajout du patient (Code: {status_code})")

# Appeler la fonction app pour exécuter l'application
app()
