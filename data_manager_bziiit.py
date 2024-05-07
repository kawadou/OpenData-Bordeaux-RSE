import requests
import streamlit as st

# URL de base de l'API bziiit
BASE_URL = "https://bziiitapi-api.azurewebsites.net"

# Fonction de récupération des labels
def get_labels():
    url = f"{BASE_URL}/opendata/labels"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        st.error(f"Échec de récupération des labels: {response.text}")
        return []

# Fonction de récupération des projets RSE
def get_rse_projects():
    url = f"{BASE_URL}/opendata/bordeaux-rse/projects"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        st.error(f"Échec de récupération des projets RSE: {response.text}")
        return []

# Fonction de récupération des entreprises
def get_engaged_brands():
    url = f"{BASE_URL}/opendata/bordeaux-rse/brands"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        st.error(f"Échec de récupération des marques engagées: {response.text}")
        return []

# Fonction consolidant les données labels + projets RSE + marques
def get_bziiit_data():
    labels = get_labels()
    rse_projects = get_rse_projects()
    engaged_brands = get_engaged_brands()

    bziiit_data = []

    # Assurez-vous d'utiliser 'name' pour bziiit data et ajoutez une distinction de type
    for label in labels:
        bziiit_data.append({
            'type': 'label',  # Ajout du type
            'name': label.get('name', 'Unknown'),
            'description': label.get('description', 'Unknown'),
            'logo_url': label.get('logo_url', 'Unknown'),
            'labels': [label]  # Stocke l'objet label entier si nécessaire
        })

    for project in rse_projects:
        bziiit_data.append({
            'type': 'project',  # Ajout du type
            'name': project.get('name', 'Unknown'),
            'labels': project.get('labels', [])  # Assurez-vous que 'labels' est une liste dans le JSON de réponse
        })

    for brand in engaged_brands:
        bziiit_data.append({
            'type': 'brand',  # Ajout du type
            'name': brand.get('name', 'Unknown'),
            'logo_url': brand.get('logo_url', 'Unknown'),  # Assurez-vous que 'logo_url' est une URL valide
            'description': brand.get('description', 'Unknown'),
            'labels': brand.get('labels', [])
        })

    return bziiit_data
