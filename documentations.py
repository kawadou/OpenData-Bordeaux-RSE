import streamlit as st

def display_documentation():

    st.markdown("<hr style='border-color: darkgrey;'>", unsafe_allow_html=True)  # Add this line

    st.title("OPEN DATA IA RSE Bordeaux Métropole")
    st.markdown("## La Data et l'IA au service des démarches RSE (Economie, Social, Environnemental)")

    st.image("DATA IA RSE Bordeaux Metropole.png", caption="Data IA RSE Bordeaux Metropole")
    st.image("RECO IA RSE Bordeaux Metropole.png", caption="RECO IA RSE Bordeaux Metropole")

    # Credits

    st.markdown("""<hr style='border-color: darkgrey;'>""", unsafe_allow_html=True)


    st.markdown("""
    <div class="credits">
        <p>Data Bordeaux Métropole : Licence MIT 2024 </p>
        <p>Data bziiit : Licence MIT 2024</p>
        <p>API IA : Perplexity</p>
        <p>Avril 2004</p>                
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()