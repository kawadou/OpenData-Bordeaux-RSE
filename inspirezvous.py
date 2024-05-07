import streamlit as st
import re
from folium import Map, Marker, Icon, Popup
from streamlit_folium import folium_static
from data_manager import get_data
from data_manager_bziiit import *
from ISO26000 import classify_actions_rse_ISO26000
from bs4 import BeautifulSoup
from urllib.parse import urlparse

###############################################################################################
# PARTIE 0 : Récupération des données API bziiit et Bordeaux Métropole
###############################################################################################

def fetch_data():
    data, _ = get_data()  # Récupération des données de Bordeaux Métropole
    bziiit_data = get_bziiit_data()  # Récupération des données de Bziiit

    return data, bziiit_data

###############################################################################################
# PARTIE 1 : Le sélecteur d'entreprise
###############################################################################################

def display_company_selection(data):
    # Get a list of all company names
    companies = sorted(list(set(record['nom_courant_denomination'] for record in data)), key=str.lower)

    selected_company = st.selectbox('Sélectionnez une entreprise', companies)
    return selected_company  # Return the selected company name

# Uniformiser les noms de champs
def normalize_company_name(record):
    # Gère les différences de noms de champs entre les APIs
    if 'nom_courant_denomination' in record:
        return record['nom_courant_denomination'].strip().lower()
    elif 'name' in record:
        return record['name'].strip().lower()
    return 'Unknown'

###############################################################################################
# PARTIE 2 : AFFICHAGE OPEN DATA BORDEAUX METROPOLE
###############################################################################################

def display_company_info(data, bziiit_data, selected_company):
    normalized_selected = normalize_company_name({'name': selected_company})  # Assurez-vous que cette fonction normalise correctement comme expliqué dans l'étape 1.
    company_data = next((record for record in data if normalize_company_name(record) == normalized_selected), None)
    bziiit_company_data = next((record for record in bziiit_data if normalize_company_name(record) == normalized_selected), None)

    classified_data = classify_actions_rse_ISO26000(data)
    # Normalize the company name for comparison
    normalized_selected = normalize_company_name({'name': selected_company})

    # Find the company in the classified data
    company_category = None
    for category, companies in classified_data.items():
        if any(normalize_company_name(company) == normalized_selected for company in companies):
            company_category = category
            break

    if bziiit_company_data is None:
        bziiit_company_data = {}

    st.markdown("""<hr style='border-color: darkgrey;'>""", unsafe_allow_html=True)
       
    if company_data:
        st.markdown("### Source OPEN DATA Bordeaux Métropole")
        st.write(f"**Nom de l'entreprise:** {company_data.get('nom_courant_denomination', 'Non disponible')}")
        
        col10, col20 = st.columns(2)

        with col10:
            if 'point_geo' in company_data and len(company_data['point_geo']) == 2:
                lat, lon = company_data['point_geo']
                m = Map(location=[lat, lon], zoom_start=10)
                popup_html = f"""
                <div style="width:300px;">
                    <b>{company_data.get('nom_courant_denomination', 'Sans nom')}</b><br><br>
                    <b>Action RSE:</b><br>
                    {company_data.get('action_rse', 'Non spécifiée')}<br><br>
                    <hr style="margin: 1px 0; border: none; border-top: 1px solid #ccc;">
                    <b>Secteur d'activité:</b> {company_data.get('libelle_section_naf', 'Non spécifié')}
                </div>
                """
                icon = Icon(icon="leaf", prefix='fa', color='green')
                Marker([lat, lon], icon=icon, popup=Popup(popup_html, max_width=500)).add_to(m)
                folium_static(m, width=330, height=500)
            else:
                st.write("**Position GPS non disponible pour cette entreprise.**")

        with col20:
            st.write(f"**Nom de l'entreprise :** {company_data.get('nom_courant_denomination', 'Non disponible')}")
            st.write(f"**Commune :** {company_data.get('commune', 'Non disponible')}")
            st.write(f"**Section NAF :** {company_data.get('libelle_section_naf', 'Non disponible')}")
            st.write(f"**Effectif :** {company_data.get('tranche_effectif_entreprise', 'Non spécifié')}")
            action_rse = company_data.get('action_rse', 'Non spécifié')
            st.write(f"**Action RSE :** {action_rse}")
        
            if action_rse != 'Non spécifié':
                if company_category:
                    st.write(f"**Classification ISO 26000 (via IA) :** {company_category}")
                else:
                    st.write("**Classification ISO 26000:** Catégorie non déterminée")

    else:
        st.error("Aucune donnée disponible pour cette entreprise depuis l'API Bordeaux Métropole.")
    
###############################################################################################
    # PARTIE 3 : AFFICHAGE OPEN DATA bziiit
###############################################################################################

    def get_labels():
        url = f"{BASE_URL}/opendata/labels"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            st.error(f"Échec de récupération des labels: {response.text}")
            return []
        
    st.markdown("""<hr style='border-color: darkgrey;'>""", unsafe_allow_html=True)    

     
    if bziiit_company_data:
        st.markdown("### Source OPEN DATA bziiit")

        # Assurez-vous d'avoir les informations nécessaires
        logo_url = bziiit_company_data.get('logo_url', '')
        website_url = bziiit_company_data.get('website_url', '')

        # Affichez le logo
        if logo_url:
            st.markdown(f'<div style="text-align: center;"><img src="{logo_url}" style="width:120px;" /></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: center;"><em style="font-size: small;">Logo non disponible</em></div>', unsafe_allow_html=True)

        # Récupérez la description
        description = bziiit_company_data.get('description', '')
        
        # Utilisez une regex pour trouver les URL dans la description
        website_url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', description)
        
        # Vérifiez si une URL a été trouvée
        if website_url:
            # Prenez la première URL trouvée
            website_url = website_url[0]
            st.markdown(f'<div style="text-align: center;">[Site web de l\'entreprise]({website_url})</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: center;"><em style="font-size: small;">URL du site web non disponible</em></div>', unsafe_allow_html=True)

        description_html = bziiit_company_data.get('description', 'Description non disponible')
        description_text = BeautifulSoup(description_html, "html.parser").get_text()
        st.write("📝 **Description de l'entreprise:**")
        st.write(description_text)

        st.markdown("🏷️ **Labels / Certifications RSE - Qualité :**")
        labels = get_labels()  # Get the labels using the get_labels function
        label_data = bziiit_company_data.get('labels', [])
        
        if not label_data:
            st.write("Pas de Labels / Certifications RSE - Qualité actuellement.")
        
        else:
            # ...
            for i in range(0, len(label_data), 2):  # Loop through labels two at a time
                cols = st.columns(2)  # Create two columns
                for j in range(2):  # Loop through the two labels
                    if i + j < len(label_data):  # Check if there is a label to process
                        label = label_data[i + j]
                        label_name = label.get("name", "Label non spécifié")
                        # Find the corresponding label in the labels data
                        label_info = next((l for l in labels if l.get("name") == label_name), None)
                        if label_info:  # Only process labels with info
                            label_description = label_info.get("description", "Description non disponible")  # Get the label description from the label info
                            logo_url = label_info.get("logo_url")  # Get the logo URL from the label info
                            try:
                                # Display the image in the corresponding column with a tooltip
                                cols[j].markdown(f'<div style="text-align: center;"><a href="#" title="{label_description}"><img src="{logo_url}" alt="{label_name}" style="width:120px;"></a><p>{label_name}</p></div>', unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Erreur lors de l'affichage de l'image : {e}")
            # ...
        if st.button('Ici pour visualiser le mail à envoyer pour référencer un nouveau label / certification RSE - Qualité'):
            st.markdown("""
                **Objet email :**  
                Demande de référencement Certification / Label RSE - Qualité  

                **Corps email :**  
                Bonjour,  

                Ci-dessous le lien publique vers la certification / label RSE - Qualité de notre entreprise pour référencement dans votre plateforme OPEN DATA IA RSE Bordeaux Métropole  

                URL à renseigner - 01 :  
                URL à renseigner - 02 :  
                URL à renseigner - 03 :  
                ...  

                Nom du demandeur :  
                Qualité ou statut :  

                Destinataire : info@bziiit.com  

                Merci par avance de votre aide pour développer la visibilité de vos Labels / Certifications
                        
                L'équipe OPEN DATA IA RSE Bordeaux Métropole
            """, unsafe_allow_html=True)

    else:
        st.write("**Aucune donnée bziiit disponible pour cette entreprise.**")


def is_valid_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False


"""
###############################################################################################
# PARTIE 5 : AFFICHAGE INSPIREZ VOUS
###############################################################################################
def display_similar_companies(data, selected_company):
    classified_data = classify_actions_rse_ISO26000(data)
    company_data = next((record for record in data if record['nom_courant_denomination'] == selected_company), None)
    if company_data:
        action_rse = company_data.get('action_rse', 'Unknown').lower()
        for category, companies in classified_data.items():
            if any(company.get('action_rse', 'Unknown').lower() == action_rse for company in companies):
"""                
#                st.markdown("""<hr style='border-color: darkgrey;'>""", unsafe_allow_html=True)
"""
                st.write("Ces organisations pourraient également vous inspirer")
                max_pages = (len(companies) - 1) // 5 + 1
                cols = st.columns([1,1,1,1,1])
                if cols[1].button('Précédent'):
                    page = max(page - 1, 1)
                page = cols[2].number_input('Page', min_value=1, max_value=max_pages, value=1, step=1)
                if cols[3].button('Suivant'):
                    page = min(page + 1, max_pages)
                
                companies_to_display = companies[(page - 1) * 5:page * 5]
                
                st.write(f"Page: {page}")  # Debugging line
                st.write(f"Companies to display: {companies_to_display}")  # Debugging line
                
                for i, company in enumerate(companies_to_display):
                    st.write(f"Company: {company}")  # Debugging line
                    logo_url = company.get('logo', 'https://opendata.bordeaux-metropole.fr/assets/theme_image/Open%20data%20-%20Pictos%2050px%20x%2050px-03.jpg')
                    if is_valid_url(logo_url):
                        cols[i].image(logo_url, width=50)
                    else:
                        cols[i].image('https://opendata.bordeaux-metropole.fr/assets/theme_image/Open%20data%20-%20Pictos%2050px%20x%2050px-03.jpg', width=50)
                    cols[i].write(f"**{company.get('name', 'Unknown')}**")
                    cols[i].write(f"{company.get('action_rse', 'Unknown')[:30]}")
"""
