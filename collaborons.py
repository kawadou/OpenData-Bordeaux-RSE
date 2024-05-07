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
# PARTIE 3 : CONNEXION API MISTRAL 8x7b + AFFICHAGE DE LA CONVERSATION
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
# PARTIE 4 : MATRICE DE MATERIALITE
###############################################################################################
def display_materiality_matrix(selected_company, data, bziiit_data):
    st.markdown("### La matrice de matérialité vue par l'IA bziiit / Mistral AI (8x7b)")
    option = st.radio(
        "Choisissez une option",
        ('Définition', 'Matrice simplifiée', 'Matrice détaillée'),
        index=0
    )

    if option == 'Définition':
        st.write("""
            **La matrice de matérialité est un outil stratégique qui permet aux entreprises de classer et de prioriser les enjeux liés à la responsabilité sociale des entreprises (RSE) selon leur importance pour les parties prenantes et leur impact sur la performance de l'entreprise. Les trois points clés de la matrice de matérialité sont :**

            1. **Évaluation et priorisation des enjeux** : La matrice de matérialité aide à identifier et à classer les enjeux RSE en fonction de leur importance pour les parties prenantes et de leur impact sur la performance de l'entreprise. Cela permet aux entreprises de se concentrer sur les enjeux qui sont les plus importants pour leurs parties prenantes et pour leur propre succès.

            2. **Transparence et communication** : La matrice de matérialité encourage la transparence en matière de RSE en offrant un cadre pour la communication des résultats aux parties prenantes. Cela permet aux entreprises de renforcer leur image de marque et de répondre aux attentes croissantes en matière de durabilité.

            3. **Flexibilité et adaptabilité** : La matrice de matérialité est adaptable à différents contextes et tailles d'entreprises, offrant une flexibilité essentielle pour répondre aux besoins variés. Elle est un élément intégral de la planification stratégique d'une entreprise et facilite un reporting ESG transparent et informatif.
        """)
    
    
    elif option == 'Matrice simplifiée':
        company_data = next((item for item in data if item['nom_courant_denomination'].strip().lower() == selected_company.strip().lower()), None)
        bziiit_brand_data = next((brand for brand in bziiit_data if brand['type'] == 'brand' and brand['name'].strip().lower() == selected_company.strip().lower()), None)
        if company_data and bziiit_brand_data:
            run_perplexity_chat_simplified(company_data['nom_courant_denomination'], bziiit_brand_data['description'], company_data['action_rse'])
    
    
    elif option == 'Matrice détaillée':
        company_data = next((item for item in data if item['nom_courant_denomination'].strip().lower() == selected_company.strip().lower()), None)
        bziiit_brand_data = next((brand for brand in bziiit_data if brand['type'] == 'brand' and brand['name'].strip().lower() == selected_company.strip().lower()), None)
        if company_data and bziiit_brand_data:
            run_perplexity_chat_detailed(company_data['nom_courant_denomination'], bziiit_brand_data['description'], company_data['action_rse'])

###############################################################################################
# PARTIE 5 : FONCTIONS MATRICE DE MATERIALITE
###############################################################################################

def run_perplexity_chat_simplified(company_name, company_description, company_rse_action):
    question = f"L'entreprise {company_name}, dont l'activité est {company_description}, a pour action RSE principale {company_rse_action}. Quels peuvent être les principaux éléments de sa matrice de matérialité ? REPONDS TOUJOURS EN FRANCAIS"
    messages = [
        {"role": "system", "content": "You are an artificial intelligence assistant and you need to engage in a helpful, detailed, polite conversation with a user."},
        {"role": "user", "content": question}
    ]
    st.markdown("**Question posée :**")
    st.write(question)
    st.markdown("**Réponse IA :**")
    perform_chat(messages)

def run_perplexity_chat_detailed(company_name, company_description, company_rse_action):
    question = f"L'entreprise {company_name}, dont l'activité est {company_description}, a pour action RSE principale {company_rse_action}. Fais moi une présentation détaillée TOUJOURS EN FRANCAISE de ce que pourraient être sa matrice de matérialité ?"
    messages = [
        {"role": "system", "content": "You are an artificial intelligence assistant and you need to engage in a helpful, detailed, polite conversation with a user."},
        {"role": "user", "content": question}
    ]
    st.markdown("**Question posée :**")
    st.write(question)
    st.markdown("**Réponse IA :**")
    perform_chat(messages)

