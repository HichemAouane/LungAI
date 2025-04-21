import numpy as np
import streamlit as st
import streamlit as st
import hydralit_components as hc
# import streamlit_analytics
from strm import Modal
import time
import json
from home import home_page
from classification import application_page
import os




def main():

    st.set_page_config(
    page_title="lung cancer classification LUNGAI",
    page_icon="🫁"
)
    st.sidebar.image("univ.png",width=200)


    with st.sidebar:
     st.title("Welcome to LungAI!")
     st.markdown(
    "LungAI est un système qui permet de classifier vos nodules pulmonaires à partir de vos fichiers MHD et RAW.<br><br>"
    "Ainsi que les coordonnées de Votre nodule<br>"
    "Ces fichiers doivent correspondre à votre CT Scan, et vos reels cordonnées<br><br>"
    "À travers l'exploration de la texture des nodules, le système LungAI permet d'évaluer vos nodules.",
    unsafe_allow_html=True
)

    st.sidebar.image("lungs.png",width=280)


    HOME = 'Home'
    APPLICATION = 'Classification'

    tabs = [
     HOME,
     APPLICATION
    ]

    option_data = [
     {'icon': "🏠", 'label': HOME},
     {'icon': "🤖", 'label': APPLICATION}

     ]

    over_theme = {
    'txc_inactive': 'black', 
    'menu_background': '#ADD8E6',  # Light blue background
    'txc_active': 'white', 
    'option_active': '#87CEEB',  # Sky blue for active option
    'menu_item_border': '2px solid #ADD8E6',  # Border to increase horizontal size
    'menu_item_margin': '10px'  # Margin to increase spacing
}
    font_fmt = {'font-class': 'h3', 'font-size': '100%'}

    chosen_tab = hc.option_bar(
       option_definition=option_data,
       title='',
       key='PrimaryOptionx',
       override_theme=over_theme,
       horizontal_orientation=True)

     
    st.markdown(
    """
    <style>
    .css-1fcdlh7 {
        max-width: 100%;
        padding: 0;
    }
    .css-1kyxreq {
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    if chosen_tab == HOME:
      home_page()


    if chosen_tab == APPLICATION: 
      application_page()

    modal = Modal(key='LungAI', title="Conditions et termes d'utilisation - LungAI", padding=50, max_width=900)

    if 'popup_closed' not in st.session_state:
      st.session_state.popup_closed = False

    if not st.session_state.popup_closed:
      with modal.container():
         st.markdown(
            'Bienvenue sur LungAI, Une bouffée d\'air frais pour vos poumons et votre esprit.En accédant et en utilisant ce site, vous acceptez les conditions suivantes :')
         st.markdown('')
         st.markdown('<strong>Intégrité du Contenu :</strong>: Les informations fournies sur LungAI'
                    'sont élaborées pour refléter un diagnostic fait par des radiologues ou des anapaths. Bien que nous nous efforçons de garantir '
                    'la précision,  cette plateforme est principalement conçue à des fins éducatives et d\'exploration.Toute ressemblance '
                    'avec des résultats scientifiques réels est purement fortuite.</br>', unsafe_allow_html=True)
         st.markdown(
            '<strong>Précision de l\'Information</strong>: Nous nous efforçons de présenter des informations avec la plus grande précision possible,mais nous ne pouvons garantir l\'exactitude absolue  ou l\'applicabilité du contenu..'
            'Veuillez considérer LungAI comme une plateforme exploratoire plutôt qu\'une source faisant autorité.</br>', unsafe_allow_html=True)
         st.markdown(
            '<strong>Conduite Responsable de l\'Utilisateur</strong>: Votre interaction avec LungAI doit être menée de manière responsable, '
            ' nous vous encourageons vivement à introduire vos informations. <br>a Tout usage abusif ou accès non autorisé est strictement interdit.</br>', unsafe_allow_html=True)

         st.markdown('<strong>Sécurité des Données</strong>: Nous prenons la sécurité de vos données très au sérieux, '
                    'Toutes les informations fournies sont traitées avec la plus grande confidentialité. '
                    'Cependant, dans l\'immensité du monde numérique, aucun système ne peut être complètement imperméable.</br>', unsafe_allow_html=True)

         st.markdown('<strong>Limitation de Responsabilité</strong>: Nous déclinons toute responsabilité quant aux conséquences de votre utilisation de LungAI. '
                    'Cela inclut, mais ne se limite pas à, des dommages directs, indirects ou consécutifs.  Pour toute préoccupation, consultez notre équipe de support.</br>', unsafe_allow_html=True)
         
         st.markdown('<strong>Modification des Conditions</strong>: Nous nous réservons le droit de modifier ces conditions sans préavis. '
                    'Votre utilisation continue de LungAI implique l\'acceptation des conditions mises à jour.Consultez régulièrement le site pour vérifier les modifications.</br>', unsafe_allow_html=True)
         st.markdown('')
         value = st.checkbox("En cliquant, vous confirmez avoir examiné et accepté ces conditions. Bonne exploration dans le monde de LungAI.")
         if value:
             close = st.button('Close')
             st.session_state.popup_closed = True
             
    

    
   
if __name__ == "__main__":
    main()


