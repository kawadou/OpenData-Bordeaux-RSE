from folium import Map, Marker, Icon, Popup
from streamlit_folium import folium_static
import streamlit as st
from data_manager import get_data

def display_map():
    data, total_hits = get_data()
    if data:
        # Ajout des titres en haut de l'écran
        st.markdown("## OPEN DATA Bordeaux Métropole RSE")
        st.markdown("### Localiser les organisations engagées RSE de Bordeaux Métropole")
        
        secteurs = sorted({record.get("libelle_section_naf") for record in data if record.get("libelle_section_naf")})
        secteur_selectionne = st.selectbox("Filtre par secteur d'activité :", ["Tous"] + secteurs)
        
        if secteur_selectionne != "Tous":
            data = [record for record in data if record.get("libelle_section_naf") == secteur_selectionne]
        
        st.markdown("Cliquer sur l'icône pour découvrir l'entreprise et une de ses actions RSE remarquable")
        
        m = Map(location=[44.84474, -0.60711], zoom_start=12)
        for item in data:
            try:
                point_geo = item.get('point_geo', [])
                if point_geo:
                    lat, lon = float(point_geo[0]), float(point_geo[1])
                    if lat and lon:
                        popup_html = f"""
                        <div style="width:300px;">
                            <b>{item.get('nom_courant_denomination', 'Sans nom')}</b><br><br>
                            <b>Action RSE:</b><br>
                            {item.get('action_rse', 'Non spécifiée')}<br><br>
                            <hr style="margin: 1px 0; border: none; border-top: 1px solid #ccc;">
                            <b>Secteur d'activité:</b> {item.get('libelle_section_naf', 'Non spécifié')}
                        </div>
                        """
                        popup = Popup(popup_html, max_width=500)
                        Marker([lat, lon], popup=popup, icon=Icon(color='green', icon='leaf', prefix='fa')).add_to(m)
            except (ValueError, TypeError, IndexError):
                continue
        
        folium_static(m)

if __name__ == "__main__":
    display_map()