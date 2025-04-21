import streamlit as st
import datetime


def home_page():
    st.divider()
    st.markdown(
        "<h1 style='text-align: center; color: black;'>LUNGAI: Classification basé sur la texture de vos Nodules Pulmonaires!</h1>",
        unsafe_allow_html=True)
    st.markdown('')
    st.image('logo.png')
    st.markdown("**Read more**: [Open access, peer-reviewed paper](https://uwaterloo.ca/vision-image-processing-lab/sites/ca.vision-image-processing-lab/files/uploads/files/2015_crv_lung_0.pdf),[Texture](https://www.sciencedirect.com/science/article/abs/pii/S1566253516301063), [CT SCAN](https://www.cancerimagingarchive.net/collection/lidc-idri/)"),
    st.markdown("")
    st.markdown('')
    st.markdown("")
    st.markdown("*Aouane Hichem, Agrane Sabrina, Department IA & SD, Université Houari Boumedienne*")
    st.markdown(" **Contact** aouane4hichem@gmail.com , sabrina.agrane1@gmail.com")
    st.divider()
    st.markdown('**Résume**')
    st.markdown(
        '<div style="text-align: justify;">LUNGAI, classification basée sur la texture de vos nodules pulmonaires a travers l\'exploration de differentes approches qui calculent des caracteristiques de textures</div>',
        unsafe_allow_html=True)

    st.divider()

    st.markdown('**Introduction**')
    st.markdown(
        "<div style='text-align: justify;'><p style='text-indent: 2em;'>"
        "Les algorithmes d'IA tels que l'apprentissage automatique, l'apprentissage profond et la radiologie ont démontré des capacités significatives dans la détection et la caractérisation des nodules pulmonaires, améliorant ainsi la précision du dépistage et du diagnostic du cancer du poumon.</p></div>",
        unsafe_allow_html=True
    )

    st.markdown('**Collecte de Données et Entraînements**')
    st.markdown(
        "<div style='text-align: justify;'><p style='text-indent: 2em;'>"
        "La base de données utilisée a été extraite de la plus grande base de données publiquement disponible pour les scans CT pulmonaires. L'entraînement de nos modèles a nécessité l\'extraction manuelle des données et l'étude des corrélations entre elles. Ce processus nous a permis d\'identifier les caractéristiques qui définissent le mieux la texture, facilitant ainsi leur classification.</p></div>",
        unsafe_allow_html=True
    )

    st.markdown('**Analyse et Synthèse**')
    st.markdown(
        "<div style='text-align: justify;'><p style='text-indent: 2em;'>"
        "L'IA présente un potentiel des plus intéressants pour améliorer la détection précoce du cancer du poumon. Nous pouvons utiliser les analyses générées par l'apprentissage automatique pour détecter les signaux tumoraux dans les données et utiliser l'apprentissage profond pour prédire les tumeurs à partir des images obtenues par tomodensitométrie.</p></div>",
        unsafe_allow_html=True
    )

    st.markdown('**Conclusion**')
    st.markdown(
        "<div style='text-align: justify;'><p style='text-indent: 2em;'>"
        "LungAI représente une avancée significative dans le diagnostic assisté par ordinateur grâce à des algorithmes d'apprentissage profond et d'apprentissage automatique. Nous sommes convaincus que cette innovation peut révolutionner les diagnostics, car les méthodes telles que la biopsie sont invasives et peuvent parfois manquer le nodule lors de l'extraction des données.</p></div>",
        unsafe_allow_html=True
    )
    st.markdown("")

