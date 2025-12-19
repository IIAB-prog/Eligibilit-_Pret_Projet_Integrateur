import streamlit as st

from Backend import predict_loan


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
    try:
        loan_status = predict_loan(client)

        if loan_status == 'Y':
            st.markdown(
                "<div style='padding:10px; background-color:green; color:white; border-radius:5px; text-align:center;'>Eligible à un prêt</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div style='padding:10px; background-color:red; color:white; border-radius:5px; text-align:center;'>Non éligible</div>",
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")

