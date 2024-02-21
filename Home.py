import streamlit as st
import requests
st.set_page_config(layout="wide")

def get_patients():
    url = 'https://hapi.fhir.org/baseR5/Patient?_count=200&_sort=-_lastUpdated'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'entry' in data:
            patient_list = []
            for patient_entry in data['entry']:
                patient = patient_entry['resource']
                patient_info = {
                    "Name": " ".join(patient.get("name", [{}])[0].get("given", ["Non disponible"])),
                    "Family Name": patient.get("name", [{}])[0].get("family", "Non disponible"),
                    "Address": patient.get("address", [{}])[0].get("text", "Non disponible"),
                    "Gender": patient.get("gender", "Non disponible") ,
                    "BirthDate": patient.get("birthDate", "Non disponible")
                }
                patient_list.append(patient_info)
            return patient_list
        else:
            st.write("Aucun patient trouvé.")
            return []
    else:
        st.error(f"Erreur lors de la récupération des données (Code: {response.status_code})")
        return []

def app():
    st.title("Liste des Patients")
    patient_data = get_patients()
    if patient_data:
        st.dataframe(patient_data)
        
        

# Appeler la fonction app pour exécuter l'application
app()
