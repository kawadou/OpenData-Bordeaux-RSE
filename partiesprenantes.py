import streamlit as st
from folium import Map, Marker, Icon, Popup
from streamlit_folium import folium_static
from data_manager import get_data
from data_manager_bziiit import *

import os
from dotenv import load_dotenv
import openai

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
def display_company_selection_for_materiality(data):
    # Get a list of all company names
    companies = sorted(list(set(record['nom_courant_denomination'] for record in data)), key=str.lower)

    # Add default selection prompt to the beginning of the list
    companies.insert(0, "Sélectionner l'entreprise engagée à découvrir")

    selected_company = st.selectbox('Sélectionnez une entreprise', companies, index=0)

    # If the default selection is still selected, return None
    if selected_company == "Sélectionner l'entreprise engagée à découvrir":
        return None

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
# PARTIE 3 : CONNEXION API sonar-medium-online + AFFICHAGE DE LA CONVERSATION
###############################################################################################

# chargement du fichier .env
load_dotenv(".streamlit/.env")

def perform_chat(messages):
    YOUR_API_KEY = os.getenv("API_TOKEN_PERPLEXITYAI")
    if YOUR_API_KEY is None:
        raise Exception("API key not found. Please check your .env configuration.")
    client = openai.OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    response_stream = client.chat.completions.create(
        model="sonar-medium-online",
        messages=messages,
        stream=True
    )

    assistant_response = ""
    for chunk in response_stream:
        assistant_response += chunk.choices[0].delta.content

    st.write(assistant_response)

###############################################################################################
# PARTIE 4 : PARTIES PRENANTES
###############################################################################################
def display_materiality_partiesprenantes(selected_company, data, bziiit_data):
    st.markdown("### Les parties prenantes identifiées par l'IA bziiit / Perplexity - sonar-medium-online")
    option = st.radio(
        "Choisissez une option",
        ('Définition', 'Parties prenantes prioritaires', 'Parties prenantes détaillées'),
        index=0
    )

    if option == 'Définition':
        st.write("""
            **L'identification et l'implication des parties prenantes dans une démarche de Responsabilité Sociale des Entreprises (RSE) sont cruciales pour le succès et la légitimité des actions entreprises. Voici une synthèse en trois points clés de leur importance :

            1. **Identification des parties prenantes pour une stratégie RSE inclusive**:
            - L'identification des parties prenantes est la première étape essentielle pour comprendre qui sont les acteurs impactés par les activités de l'entreprise et qui peuvent influencer ses décisions[4].
            - Cela inclut un large éventail d'acteurs tels que les employés, clients, fournisseurs, actionnaires, communautés locales, ONG et l'État[4][5].
            - La norme ISO 26000 recommande d'intégrer les parties prenantes à tous les niveaux de la démarche RSE, ce qui permet de reconnaître et de répondre à leurs intérêts et attentes[3][5].

            2. **Hiérarchisation et cartographie pour prioriser les actions**:
            - Après l'identification, il est important de qualifier et de hiérarchiser les parties prenantes pour déterminer leur influence et leurs attentes, ainsi que les impacts de l'entreprise sur eux[4].
            - La cartographie des parties prenantes permet de visualiser et de prioriser les relations en fonction de leur importance stratégique pour l'entreprise[2].
            - Cette étape aide à concentrer les ressources et les efforts sur les parties prenantes clés et à élaborer des stratégies d'engagement adaptées[2][4].

            3. **Engagement des parties prenantes pour une RSE efficace et crédible**:
            - L'engagement des parties prenantes est fondamental pour construire une démarche RSE crédible et pour obtenir leur soutien[4][5].
            - Il s'agit d'établir un dialogue constructif, de définir des objectifs SMART et de mettre en place des actions concrètes pour répondre aux attentes des parties prenantes[4].
            - L'implication active des parties prenantes internes et externes favorise la transparence, renforce la confiance et améliore l'acceptabilité sociale des activités de l'entreprise[6].

            En somme, l'identification et l'implication des parties prenantes sont des processus interdépendants qui permettent aux entreprises de développer une stratégie RSE cohérente, de gérer les risques et d'optimiser leur impact social et environnemental.

            Citations:
            [1] https://www.greenflex.com/actualites/articles/rse-parties-prenantes/
            [2] https://datavalue-consulting.com/cartographie-partie-prenante-rse/
            [3] https://www.novethic.fr/entreprises-responsables/qui-sont-les-parties-prenantes-de-lentreprise.html
            [4] https://www.cabinetdesaintfront.fr/publications/comment-engager-ses-parties-prenantes/
            [5] https://www.labellucie.com/parties-prenantes-rse
            [6] https://blog.hubspot.fr/marketing/parties-prenantes-rse
            [7] https://www.erudit.org/fr/revues/mi/2013-v17-n2-mi0560/1015400ar/
            [8] https://www.civitime.com/rse/parties-prenantes
            [9] https://speaknact.fr/fr/blog/article/561--impliquer-ses-parties-prenantes-pour-une-rse-efficace
            [10] https://www.abeautifulgreen.com/le-role-des-parties-prenantes-et-la-rse/
            [11] https://www.cairn.info/revue-management-et-avenir-2014-2-page-73.htm
            [12] https://www.squadeasy.com/blog/qui-sont-les-parties-prenantes-dune-entreprise
            [13] https://www.associatheque.fr/fr/fichiers/bao/fiche-memo-RSE-DD-les-etapes-de-la-demarche.pdf
            [14] https://greenly.earth/fr-fr/blog/guide-entreprise/rse-partie-prenantes
            [15] https://www.veolia.com/fr/veolia-group/engagement-rse/engagement-parties-prenantes                 

       """)
    
    
    elif option == 'Parties prenantes prioritaires':
        company_data = next((item for item in data if item['nom_courant_denomination'].strip().lower() == selected_company.strip().lower()), None)
        bziiit_brand_data = next((brand for brand in bziiit_data if brand['type'] == 'brand' and brand['name'].strip().lower() == selected_company.strip().lower()), None)
        if company_data and bziiit_brand_data:
            run_perplexity_chat_parties_prenantes_prioritaires(company_data['nom_courant_denomination'], bziiit_brand_data['description'], company_data['action_rse'])
    
    
    elif option == 'Parties prenantes détaillées':
        company_data = next((item for item in data if item['nom_courant_denomination'].strip().lower() == selected_company.strip().lower()), None)
        bziiit_brand_data = next((brand for brand in bziiit_data if brand['type'] == 'brand' and brand['name'].strip().lower() == selected_company.strip().lower()), None)
        if company_data and bziiit_brand_data:
            run_perplexity_chat_parties_prenantes_detailed(company_data['nom_courant_denomination'], bziiit_brand_data['description'], company_data['action_rse'])

###############################################################################################
# PARTIE 5 : FONCTIONS PARTIES PRENANTES
###############################################################################################

def run_perplexity_chat_parties_prenantes_prioritaires(company_name, company_description, company_rse_action):
    question = f"En tant que spécialiste RSE et notamment de l'identification des parties prenantes d'une entreprise, tu es chargé d'identifier les parties prenantes prioritaires de l'entreprise dont : le nom est {company_name}, l'activité est {company_description}, ses principales actions RSE sont {company_rse_action}. Affiche les résultats TOUJOURS EN FRANCAIS classés par catégories de parties prenantes et cite les sources en bas de ta réponse."
    messages = [
        {"role": "system", "content": "You are an artificial intelligence assistant and you need to engage in a helpful, detailed, polite conversation with a user."},
        {"role": "user", "content": question}
    ]
    st.markdown("**Question posée :**")
    st.write(question)
    st.markdown("**Réponse IA :**")
    perform_chat(messages)

def run_perplexity_chat_parties_prenantes_detailed(company_name, company_description, company_rse_action):
    question = f"En tant que spécialiste RSE et notamment de l'identification des parties prenantes d'une entreprise, tu es chargé d'identifier l'ensemble des parties prenantes de l'entreprise dont : le nom est {company_name}, l'activité est {company_description}, ses principales actions RSE sont {company_rse_action},. Affiche les résultats détaillés  TOUJOURS EN FRANCAIS classés par catégories de parties prenantes et cite les sources en bas de ta réponse."
    messages = [
        {"role": "system", "content": "You are an artificial intelligence assistant and you need to engage in a helpful, detailed, polite conversation with a user."},
        {"role": "user", "content": question}
    ]
    st.markdown("**Question posée :**")
    st.write(question)
    st.markdown("**Réponse IA :**")
    perform_chat(messages)

