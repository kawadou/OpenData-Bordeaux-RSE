import streamlit as st
from data_manager_bziiit import get_bziiit_data

def display_labelled_companies():
    st.markdown("## Entreprises Labellisées (source OPEN DATA bziiit)")
    st.markdown("### Découvrez les entreprises engagées avec au moins un label RSE")

    # Récupération des données bziiit
    bziiit_data = get_bziiit_data()

    # Filtrage des entreprises ayant au moins un label
    labelled_companies = [brand for brand in bziiit_data if brand['type'] == 'brand' and len(brand.get('labels', [])) > 0]

    # Calcul du nombre de labels par entreprise
    for brand in labelled_companies:
        brand['label_count'] = len(brand['labels'])

    # Calcul et affichage du nombre et du pourcentage d'entreprises labellisées
    total_companies = len([brand for brand in bziiit_data if brand['type'] == 'brand'])
    labelled_companies_count = len(labelled_companies)
    percentage_labelled = round((labelled_companies_count / total_companies) * 100)
    st.markdown(f"**Nb entreprises labellisées :** {labelled_companies_count} ({percentage_labelled}%)")

    # Tri des entreprises par le nombre de labels, ordre décroissant
    labelled_companies.sort(key=lambda x: x['label_count'], reverse=True)

    # Affichage des entreprises
    for i in range(0, len(labelled_companies), 5):
        cols = st.columns(5)
        image_placeholders = [col.empty() for col in cols]
        padding_placeholders = [col.empty() for col in cols]
        text_placeholders = [col.empty() for col in cols]
        for j in range(5):
            if i + j < len(labelled_companies):
                company = labelled_companies[i + j]
                with cols[j]:
                    if company['logo_url'] != 'Unknown':
                        image_placeholders[j].image(company['logo_url'], width=100)
                    padding_placeholders[j].write("")  # This will act as padding
                    text_placeholders[j].write(company['name'])
                    text_placeholders[j].write(f"Nb labels : {company['label_count']}")



    
