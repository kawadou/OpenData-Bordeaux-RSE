import streamlit as st
from collections import Counter

from data_manager import get_data
from data_manager_bziiit import get_labels, get_engaged_brands

def display_rse_labels():
    st.markdown("## OPEN DATA bziiit Labels RSE")
    st.markdown("### Découvrez  les labels et certifications (RSE, Qualité...)")

    labels_option = st.radio(
        "Choisissez les labels à afficher :",
        ("Labels / Certifications des organisations engagées Bdx Métropole", "Tous les labels / Certifications DATA bziiit")
    )

    
    st.markdown("""<hr style='border-color: darkgrey;'>""", unsafe_allow_html=True)

    labels = get_labels()
   
    if labels_option == "Tous les labels / Certifications DATA bziiit":
        labels.sort(key=lambda x: x['name'])
    else:
        # Get the data from Bordeaux Metropole API
        data, _ = get_data()

        # Get the engaged brands
        engaged_brands = get_engaged_brands()

        # Get the names of the organizations from Bordeaux Metropole API
        org_names = set(org['nom_courant_denomination'] for org in data if 'nom_courant_denomination' in org)

        # Filter the engaged brands to include only the organizations in Bordeaux Metropole
        engaged_brands = [brand for brand in engaged_brands if brand['name'] in org_names]

        # Get the labels used by the organizations
        org_labels = [label['name'] for brand in engaged_brands if 'labels' in brand and brand['labels'] for label in brand['labels']]

        # Count the labels
        label_counts = Counter(org_labels)

        # Filter the labels and add the count
        labels = [{'name': label['name'], 'logo_url': label['logo_url'], 'count': label_counts[label['name']]} for label in labels if label['name'] in label_counts]

        # Sort the labels by count in descending order
        labels.sort(key=lambda x: x['count'], reverse=True)

    # Display the total number of unique labels
    unique_labels = set(label['name'] for label in labels)
    st.markdown(f"**Nombre de labels / certifications :** {len(unique_labels)}")

    # Display the labels
    for i in range(0, len(labels), 5):
        cols = st.columns(5)
        for j in range(5):
            if i + j < len(labels):
                label = labels[i + j]
                with cols[j]:
                    st.image(label['logo_url'])
                    if labels_option == "Tous les labels / Certifications DATA bziiit":
                        st.markdown(f'<p style="text-align: center; font-size: 10px;"><a href="{label["website"]}" style="color: darkgray;">Site web</a></p>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<p style="text-align: center; font-size: 10px; color: darkgray;">Nb marques certifiées : {label["count"]}</p>', unsafe_allow_html=True)
