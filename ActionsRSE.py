import streamlit as st
import data_manager

def display_actions_rse():
    # Utilisation de data_manager pour récupérer les données
    data, total_hits = data_manager.get_data()
    
    if total_hits > 0:
        # Ajout des titres en haut de l'écran, similaires à organisations_engagees.py mais avec un texte personnalisé
        st.markdown("## OPEN DATA Bordeaux Métropole RSE")
        st.markdown("### Découvrer les actions RSE des organisations engagées de Bordeaux Métropole")
        
        secteurs = sorted({record.get("libelle_section_naf") for record in data if record.get("libelle_section_naf")})
        secteur_selectionne = st.selectbox("Filtre par secteur d'activité :", ["Tous"] + secteurs)
        
        # Filtrage des actions RSE basé uniquement sur le secteur sélectionné
        actions_filtrees = [
            record for record in data
            if record.get("libelle_section_naf") == secteur_selectionne or secteur_selectionne == "Tous"
        ]
        
        # Affichage des actions RSE filtrées
        if actions_filtrees:
            for action in actions_filtrees:
                # Utilisation de Markdown pour l'affichage enrichi, incluant le gras
                st.markdown(f":green_heart: **Entreprise**: {action.get('nom_courant_denomination')}\n\n**Action**: {action.get('action_rse')}", unsafe_allow_html=True)
        else:
            st.write("Aucune action RSE correspondante trouvée.")
        
        # Afficher le total des actions RSE
        st.markdown(f"**Total des actions RSE :** {len(actions_filtrees)}")
        
    else:
        st.write("Erreur lors de la récupération des données.")
