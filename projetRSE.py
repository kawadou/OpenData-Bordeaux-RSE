import streamlit as st
import re  # Importer la bibliothèque pour les expressions régulières
from data_manager_bziiit import get_rse_projects

def remove_html_tags(text):
    """Supprimer les balises HTML d'une chaîne de caractères."""
    clean_text = re.sub('<.*?>', '', text)  # Remplacer toute balise HTML par une chaîne vide
    return clean_text

def display_rse_projects():
    st.markdown("""
        <style>
            table {
                background-color: inherit !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("## OPEN DATA bziiit Projet RSE")
    st.markdown("### Découvrez tous les projets RSE des marques référencées")
    
    projects = get_rse_projects()
    if projects:
        categories = list({project["rse_category"] if project["rse_category"] is not None else "Non catégorisé" for project in projects})
        categories.sort()
        categories.insert(0, 'Toutes')
        selected_category = st.selectbox("Filtre par catégorie RSE", categories, index=0)

        if selected_category != 'Toutes':
            filtered_projects = [project for project in projects if project["rse_category"] == selected_category or (selected_category == "Non catégorisé" and project["rse_category"] is None)]
        else:
            filtered_projects = projects

        st.markdown(f"**Nombre de projets :** {len(filtered_projects)}")

    # Display the projects as thumbnails
    for i in range(0, len(filtered_projects), 5):
        cols = st.columns(5)
        for j in range(5):
            if i + j < len(filtered_projects):
                project = filtered_projects[i + j]
                with cols[j]:
                    if project['logo_url']:  # Ajouter cette vérification ici
                        st.image(project['logo_url'])
                    st.markdown(f'<p style="text-align: center;"><b>{project["brand"]["name"]}</b></p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align: center;"><b>"{project["name"]}"</b></p>', unsafe_allow_html=True)  # Ajouter cette ligne
                    st.markdown(f'<p style="text-align: center; font-size: 10px; color: darkgray;">{project["rse_category"] if project["rse_category"] is not None else "Non catégorisé"}</p>', unsafe_allow_html=True)
        st.markdown('<hr style="border-top: 1px dotted lightgray; width:100%;">', unsafe_allow_html=True)  # Modifier cette ligne