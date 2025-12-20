import streamlit as st
import requests
import json

st.title("Prédicteur d'éligibilité au prêt bancaire")

client = {}

# =========================
# GENRE (FR affiché / EN stocké)
# =========================
gender_label = st.selectbox(
    "Genre",
    ["Homme", "Femme", "Personne morale"]
)

gender_map = {
    "Homme": "Male",
    "Femme": "Female",
    "Personne morale": "Morale"
}
client["Gender"] = gender_map[gender_label]

# =========================
# Champs conditionnels
# =========================
if client["Gender"] != "Morale":
    married_label = st.selectbox("Marié(e)", ["Oui", "Non"])
    client["Married"] = "Yes" if married_label == "Oui" else "No"

    education_label = st.selectbox(
        "Niveau d’éducation",
        ["Diplômé", "Non diplômé"]
    )
    client["Education"] = "Graduate" if education_label == "Diplômé" else "Not Graduate"

    self_employed_label = st.selectbox(
        "Travailleur indépendant(e)",
        ["Oui", "Non"]
    )
    client["Self_Employed"] = "Yes" if self_employed_label == "Oui" else "No"

# =========================
# Champs toujours visibles
# =========================
client["Dependents"] = st.selectbox(
    "Personnes à charge",
    ["0", "1", "2", "3+"]
)

client["ApplicantIncome"] = st.number_input(
    "Revenu du candidat (en dollars $)",
    min_value=0
)

client["CoapplicantIncome"] = st.number_input(
    "Revenu du co-candidat (en dollars $)",
    min_value=0
)

client["LoanAmount"] = st.number_input(
    "Montant du prêt (en dollars $)",
    min_value=0
)

client["Loan_Amount_Term"] = st.number_input(
    "Durée du prêt (en mois)",
    min_value=0
)

credit_label = st.selectbox(
    "Historique de crédit (respect des engagements)",
    ["Non", "Oui"]
)
client["Credit_History"] = 1 if credit_label == "Oui" else 0

property_label = st.selectbox(
    "Zone de la propriété",
    ["Urbaine", "Semi-urbaine", "Rurale"]
)

property_map = {
    "Urbaine": "Urban",
    "Semi-urbaine": "Semiurban",
    "Rurale": "Rural"
}
client["Property_Area"] = property_map[property_label]

# =========================
# Bouton de prédiction
# =========================
if st.button("Résultat d'éligibilité"):
    url = "https://api-pret-bancaire.onrender.com/predict"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(client), headers=headers)

    if response.status_code == 200:
        result = response.json()
        loan_status = result["Loan_Status"]

        if loan_status == "Y":
            st.markdown(
            f"""
             <div style='padding:15px; background-color:green; color:white;
             border-radius:8px; text-align:center;'>
             <b>Éligible à un prêt bancaire</b><br>
             <span style='font-size:14px;'>
             Probabilité d’acceptation : <b>{probability*100:.2f} %</b>
             </span>
             </div>
             """,
             unsafe_allow_html=True
         )
        else:
             st.markdown(
             f"""
             <div style='padding:15px; background-color:red; color:white;
             border-radius:8px; text-align:center;'>
             <b>Non éligible au prêt bancaire</b><br>
             <span style='font-size:14px;'>
             Probabilité d’acceptation : <b>{probability*100:.2f} %</b>
             </span>
             </div>
             """,
             unsafe_allow_html=True
             )

        else:
             st.error("Erreur lors de la communication avec l’API")



