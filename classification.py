import pickle
import random
import time
import streamlit as st
from streamlit_searchbox import st_searchbox
from utils import *
import os
import shutil
import tensorflow as tf
from tensorflow import *
from ExtractionManuelle import *
import fuctions
import tensorflow as tf
def update_selection(option):
        st.session_state.selected_option = option 
def application_page():
     if os.path.exists(f'TempFiles'):
        # Supprimez le dossier existant
          shutil.rmtree('TempFiles')
    
    # Créez un nouveau dossier vide
     os.makedirs('TempFiles')
     st.write(page_title="Lung Module Classification", page_icon="🫁", layout="wide")
     # Display the logo
     # Center and enlarge the logo using columns
     col1, col2, col3 = st.columns([1, 1, 1])

     st.markdown(f'<h1 class="text">☁️ Upload your CT Scan :</h1>',unsafe_allow_html=True)
     st.markdown('<h3 style="color: #1212a1;">Upload MHD File</h3>', unsafe_allow_html=True)

    # Upload MHD file
     mhd_file = st.file_uploader("Upload an MHD file", type=["mhd"])

     if mhd_file:
            st.session_state['mhd_file'] = mhd_file
            st.success(".mhd File uploaded successfully")
            save_uploaded_file(mhd_file)

     st.markdown('<h3 style="color: #1212a1;">Upload RAW File</h3>', unsafe_allow_html=True)

    # Upload RAW file
     raw_file = st.file_uploader("Upload a RAW file", type=["raw"])

     if raw_file:
            st.session_state['raw_file'] = raw_file
            st.success(".raw File uploaded successfully")
            save_uploaded_file(raw_file)

#------------------------------------------------------------------------------------------------------------------------------

     # Input coordinates
     st.markdown("<hr style='border:1px solid gray;margin:20px 0;'>", unsafe_allow_html=True)
     st.markdown("<h1><span >📍 Nodule Coordinates :</span></h1>",unsafe_allow_html=True)
     x = st.number_input("X Coordinate", min_value=-1924.00000, max_value=1924.00000, value=0.00000, step=1.00000, format="%.5f")
     y = st.number_input("Y Coordinate", min_value=-1924.00000, max_value=1924.00000, value=0.00000, step=1.00000, format="%.5f")
     z = st.number_input("Z Coordinate", min_value=-1924.00000, max_value=1924.00000, value=0.00000, step=1.00000, format="%.5f")
     # Utiliser la classe CSS dans le texte markdown avec l'emoji
     if st.button("Zoom"):
            if 'mhd_file' not in st.session_state:
              st.error("Please upload an MHD file")
            if 'raw_file' not in st.session_state:
              st.error("Please upload a RAW file")
            if not x and not y and not z:
               st.error("Please enter the coordinates of the nodule")
            else:
              Slice = os.path.join('TempFiles', mhd_file.name)
              Zoom(Slice, x, y, z)
              st.image('TempFiles/Zoom.png')
              st.markdown("<h6><span style='font-size: 24px; color:#FF0000;'>Note: Veuillez confirmer que le nodule est au centre de l'image avant de continuer.</span></h6>", unsafe_allow_html=True)
     st.markdown("<hr style='border:1px solid gray;margin:20px 0;'>", unsafe_allow_html=True)
#----------------------------------------------------------------------------------------------------------------------------------------

     if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
       
     st.markdown(f'<h1 class="text">🤖Choisisez votre approche :</h1>',unsafe_allow_html=True)
     st.markdown(f'<h2 class="text">Quels Methode voulez vous utilisez pour extraite des caracteristiques?:</h2>',unsafe_allow_html=True)
     option = st.radio('',('Automatic 🧠', 'Manual ⚙️'))
     if option == 'Manual ⚙️':
       st.markdown(f'<h4 class="text">Quels Approches Voulez vous utiliser pour analyser le nodule ?:</h4>',unsafe_allow_html=True)
       methode = st.radio('',('GLCM', 'Local binary patern', 'Histogram of oriented gradients', 'Gabor filter and HU'))
       st.markdown(f'<h4 class="text">Quels Models voulez vous utiliser pour classifier le nodule ?:</h4>',unsafe_allow_html=True)
       model = st.radio('',('KNN', 'SVM'))

     if st.button("Process"):
        if 'mhd_file' not in st.session_state:
              st.error("Please upload an MHD file")
        if 'raw_file' not in st.session_state:
               st.error("Please upload a RAW file")
        if not x and not y and not z:
               st.error("Please enter the coordinates of the nodule")
        else:
              file = os.path.join('TempFiles', mhd_file.name)
              if option == 'Automatic 🧠':
                genfileDL(file, x, y, z)
                img = np.load('TempFiles/chunk.npy')
                img = np.expand_dims(img, axis=-1)
                img = np.expand_dims(img, axis=0)
                cnn = tf.keras.models.load_model('models/CNN++.h5')
                cnn.load_weights('models/CNN++.weights.h5')
                cnn.predict(img)

                if cnn.predict(img)[0][0]> cnn.predict(img)[0][1]:
                   st.markdown(f'<h1 class="text">🧫Classification du nodule:</h1>',unsafe_allow_html=True)
                   st.markdown(f'<h2 class="text" Style="color: #008000;">Benin</h2>',unsafe_allow_html=True)
                else:
                  st.markdown(f'<h1 class="text">🧫Classification du nodule:</h1>',unsafe_allow_html=True)
                  st.markdown(f'<h2 class="text" Style="color: #ff0000;">Malin</h2>',unsafe_allow_html=True)
                
              if option == 'Manual ⚙️':
                  chunk =genfile(file, x,y,z)
                  mod = ChoixClassification(methode, model)
                  resultat = Prediction(methode,mod,chunk)
                  st.markdown("<hr style='border:1px solid gray;margin:20px 0;'>", unsafe_allow_html=True)
                  st.markdown(f'<h1 class="text">🧫Classification du nodule:</h1>',unsafe_allow_html=True)
                  st.markdown(f'<h6 class="text".></h6>',unsafe_allow_html=True)
                  if resultat == 1:
                            st.markdown(f'<h2 class="text" Style="color: #ff0000;">Malin</h2>',unsafe_allow_html=True)
                  elif resultat == 0:
                            st.markdown(f'<h2 class="text" Style="color: #008000;">Benin</h2>',unsafe_allow_html=True)
