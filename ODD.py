
from data_manager import get_data

def classify_actions_rse_ODD(data):
    data, _ = get_data()  # Assuming the function get_data() retrieves the RSE action data

    # Definition of the 17 SDGs and their associated keywords
    odd_criteria = {
        "ODD 1: No Poverty": ["pauvreté", "précarité", "aide financière"],
        "ODD 2: Zero Hunger": ["faim", "sécurité alimentaire", "nutrition"],
        "ODD 3: Good Health and Well-being": ["santé", "bien-être", "soins médicaux", "vaccination"],
        "ODD 4: Quality Education": ["éducation", "apprentissage", "école", "alphabétisation"],
        "ODD 5: Gender Equality": ["égalité des sexes", "femmes", "droits des femmes"],
        "ODD 6: Clean Water and Sanitation": ["eau propre", "sanitation", "hygiène"],
        "ODD 7: Affordable and Clean Energy": ["énergie renouvelable", "énergie propre", "efficacité énergétique"],
        "ODD 8: Decent Work and Economic Growth": ["emploi", "travail décent", "croissance économique"],
        "ODD 9: Industry, Innovation, and Infrastructure": ["industrie", "innovation", "infrastructure"],
        "ODD 10: Reduced Inequalities": ["inégalités", "justice sociale", "équité"],
        "ODD 11: Sustainable Cities and Communities": ["développement urbain", "communauté durable", "urbanisme"],
        "ODD 12: Responsible Consumption and Production": ["consommation durable", "production durable", "recyclage"],
        "ODD 13: Climate Action": ["climat", "réchauffement global", "émissions"],
        "ODD 14: Life Below Water": ["océans", "mers", "aquatique"],
        "ODD 15: Life on Land": ["terrestre", "biodiversité", "déforestation"],
        "ODD 16: Peace, Justice, and Strong Institutions": ["paix", "justice", "institution"],
        "ODD 17: Partnerships for the Goals": ["partenariat", "coopération internationale", "synergie"]
    }

    # Initialize dictionary to store classification results
    classified_data = {odd: [] for odd in odd_criteria}

    # Classify each RSE action based on ODD keywords
    for record in data:
        if 'description' in record:
            description = record['description'].lower()
            for odd, keywords in odd_criteria.items():
                if any(keyword in description for keyword in keywords):
                    classified_data[odd].append(record)

    return classified_data

# Example of using the function with some mock data
data_example = [
    {"description": "L'entreprise fournit une aide financière pour lutter contre la pauvreté."},
    {"description": "Programme de nutrition pour éliminer la faim."},
    {"description": "Nouvelle politique d'emploi pour promouvoir le travail décent et la croissance économique."}
]
classified_results = classify_actions_rse_ODD(data_example)
print(classified_results)



