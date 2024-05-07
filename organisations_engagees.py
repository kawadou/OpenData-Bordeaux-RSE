import streamlit as st
import pandas as pd
from data_manager import get_data

# Fonction pour l'onglet "Organisations engagées"
def display_organisations_engagees():
    st.markdown("## OPEN DATA Bordeaux Métropole RSE")
    st.markdown("### Découvrez les organisations engagées RSE de Bordeaux Métropole")
    
    data, total_hits = get_data()
    if data:
        # Calcul du nombre total d'organisations
        st.markdown(f"Nombre d'organisations : {total_hits}")
        
        df = pd.DataFrame(data)
        df = df.rename(columns={
            "nom_courant_denomination": "Nom",
            "commune": "Commune",
            "libelle_section_naf": "Section NAF",
            "tranche_effectif_entreprise": "Effectif",
            "action_rse": "Action RSE"
        })
        df = df[["Nom", "Commune", "Section NAF", "Effectif", "Action RSE"]]
        st.dataframe(df, width=None, height=None)
