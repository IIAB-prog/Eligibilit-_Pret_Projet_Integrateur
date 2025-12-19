import streamlit as st
import requests
import json

st.title("Prédicteur d'éligibilité au prêt")

# Formulaire client
# Formulaire client
client = {}

# Sélection du genre
client['Gender'] = st.selectbox("Genre", ["Male", "Female", "Morale"])

# Afficher les autres champs uniquement si ce n'est pas "Morale"
if client['Gender'] != "Morale":
    client['Married'] = st.selectbox("Marié(e)", ["Yes", "No"])
    client['Education'] = st.selectbox("Education", ["Graduate", "Not Graduate"])
    client['Self_Employed'] = st.selectbox("Travailleur indépendant(e)", ["Yes", "No"])

# Champs toujours visibles
client['Dependents'] = st.selectbox("Personnes à charge (Nombre d'employé)", ["0", "1", "2", "3+"])
client['ApplicantIncome'] = st.number_input("Revenu du candidat", min_value=0)
client['CoapplicantIncome'] = st.number_input("Revenu du co-candidat", min_value=0)
client['LoanAmount'] = st.number_input("Montant du prêt", min_value=0)
client['Loan_Amount_Term'] = st.number_input("Durée du prêt", min_value=0)
client['Credit_History'] = st.selectbox("Historique de crédit (respect des directives)", [0, 1])
client['Property_Area'] = st.selectbox("Propriété_Zone", ["Urban", "Semiurban", "Rural"])

# Bouton de prédiction
if st.button("Résultat d'éligibilité"):
    url = "https://api-pret-bancaire.onrender.com"  # ton API Flask
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(client), headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        loan_status = result['Loan_Status']
        
        if loan_status == 'Y':
            st.markdown(f"<div style='padding:10px; background-color:green; color:white; border-radius:5px; text-align:center;'>Eligible à un prêt</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='padding:10px; background-color:red; color:white; border-radius:5px; text-align:center;'>Non éligible</div>", unsafe_allow_html=True)
        
    else:
        st.error("Erreur lors de la communication avec l’API")
