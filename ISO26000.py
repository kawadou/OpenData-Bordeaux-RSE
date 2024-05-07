from data_manager import get_data

def classify_actions_rse_ISO26000(data):
    data, _ = get_data()  # Récupérer les données depuis data_manager.py
    
    criteria = {
        "Gouvernance de la structure": [],
        "Droits humains": [],
        "Conditions et relations de travail": [],
        "Responsabilité environnementale": [],
        "Loyauté des pratiques": [],
        "Questions relatives au consommateur": [],
        "Communautés et développement local": [],
        "Autres": [] 
    }

    # Keywords for each ISO 26000 category to help in classifying the actions
    keywords = {
        "Gouvernance de la structure": ["gouvernance", "structure", "organisation","leadership", "processus décisionnel", "responsabilité", "transparence", "éthique","entreprise à mission", "éthique d'entreprise", "transparence", "gouvernance responsable", "statuts", "loi pacte", "charte éthique","politique RSE dans la durée", "sens à la mission","fresque du climat"],
        "Droits humains": ["droits humains", "droit", "humains","non-discrimination", "libertés fondamentales", "droits civils et politiques", "droits économiques, sociaux et culturels", "groupes vulnérables","humain au centre","lutter contre les discriminations"],
        "Conditions et relations de travail": ["conditions de travail", "relations de travail", "emploi", "emploi et relations employeur-employé", "conditions de travail et protection sociale", "dialogue social", "santé et sécurité au travail", "développement des ressources humaines","télétravail", "semaine de 4 jours", "bien-être", "formation RSE", "sensibilisation RSE", "inclusion sociale", "diversité", "équilibre vie professionnelle", "qualité de vie au travail","inclusion des femmes","centrer sur l'humain","engagement des équipes"],
        "Responsabilité environnementale": ["environnement", "écologie", "durable","prévention de la pollution", "utilisation durable des ressources", "atténuation et adaptation au changement climatique", "protection de l'environnement, de la biodiversité et restauration des habitats naturels","carbone", "véhicules électriques", "plantation d'arbres", "réduction plastique", "compost", "gestion de l'eau", "énergies renouvelables", "réduction émissions", "déchets", "recyclage", "mobilité durable", "transport en commun", "réutilisation", "reconditionné", "panneaux solaires","véhicules électriques","vélo électrique", "mobilité durable","décarbonation","réduction consommation d'eau","véhicules hybrides","véhicules hydrides","consommation d'eau"],
        "Loyauté des pratiques": ["loyauté", "éthique", "pratiques","lutte contre la coruption", "comportement éthique", "concurrence loyale", "promotion de la responsabilité sociale dans la chaîne de valeur", "respect des droits de propriété","pratiques loyales en matière de marketing, d'information et de contrats", "protection de la santé et de la sécurité des consommateurs", "consommation durable", "service et assistance après-vente", "protection et confidentialité des données des consommateurs","commerce équitable", "marketing éthique", "droits des consommateurs", "transparence des informations", "pratiques loyales", "fournisseurs locaux","partenaires de proximité"],
        "Questions relatives au consommateur": ["consommateur", "client", "service","service client", "protection du consommateur", "consommation responsable", "satisfaction client", "qualité des produits et services", "sécurité des produits et services", "information et éducation des consommateurs", "santé et sécurité des consommateurs", "service après-vente", "garantie", "retour produit", "éthique des affaires", "commerce équitable", "marketing éthique", "droits des consommateurs", "transparence des informations", "pratiques loyales"],
        "Communautés et développement local": ["communauté", "développement local", "société","implication de la communauté", "éducation et culture", "création d'emplois et développement des compétences", "développement des technologies", "création de richesse et de revenus","engagement communautaire", "développement local", "actions caritatives", "événements sportifs", "soutien aux associations", "inclusion sociale", "lutte contre les discriminations", "coopération locale", "soutien à l'économie locale","écosystèmes sportifs", "touristiques", "culturels", "1% for the planet","préservation site", "dynamisation communauté","commun sportif", "transmission", "formations"],
  
    }

    for record in data:
        action_rse = record.get("action_rse", "").lower()
        company_info = {
            "name": record.get("nom_courant_denomination", "N/A"),
            "action_rse": action_rse,
            "activity": record.get("libelle_section_naf", "N/A"),
            "city": record.get("commune", "N/A")
        }
        found_category = False
        for criterion, key_phrases in keywords.items():
            if any(key_phrase in action_rse for key_phrase in key_phrases):
                criteria[criterion].append(company_info)
                found_category = True
                break  # Assuming each action belongs to one category only
        
        # Si l'action n'a pas été classifiée dans une catégorie existante, la placer dans "Autres"
        if not found_category:
            criteria["Autres"].append(company_info)

    return criteria