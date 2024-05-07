import requests

# URL de base de l'API bziiit
def get_data():
    url = "https://opendata.bordeaux-metropole.fr/api/records/1.0/search/?dataset=met_etablissement_rse&q=&rows=100"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        records = data.get("records", [])
        if records:
            print(records[0])  # Print an example record
        # Ensure every record includes the 'nom_courant_denomination' key
        for record in records:
            if 'nom_courant_denomination' not in record["fields"]:
                record["fields"]['nom_courant_denomination'] = 'Unknown'
        return [record["fields"] for record in records], data.get("nhits", 0)
    else:
        return [], 0

"""
Exemple de données récupérées via l'API de Bordeaux Métropole:

st.write("Normalized Company Data:", company_data)

Normalized Company Data:

{
"point_geo":[
0:44.88136729281935
1:-0.5145680443292318
]
"tranche_effectif_etab":"Non déclaré"
"siret":"8,1383E+13"
"naf_section":"J"
"code_naf":"6510Z"
"ban_x_lambert_93":422559.4
"code_postal":"33310"
"naf_groupe":"620"
"libelle_section_naf":"Information et communication"
"libelle_groupe_naf":"Programmation, conseil et autres activités informatiques"
"nom_courant_denomination":"bziiit"
"tranche_effectif_entreprise":"6 à 9 Salariés"
"commune":"LORMONT"
"action_rse":"Face à l'urgence de réduire l'empreinte carbone du numérique, nous avons mis en place le tryptique MESURER - FORMER - REDUIRE sur l'ensemble de nos usages (cloud, intelligence artificielle)"
"hierarchie_naf":"Information et communication/Programmation, conseil et autres activités informatiques/libelle_naf"
"adresse_numero_et_voie":"6 Rue du Courant"
"ban_y_lambert_93":6426418.2
}

"""