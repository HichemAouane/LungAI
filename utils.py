import numpy as np
import os
import streamlit as st
from ExtractionManuelle import *
def load_mhd_file(file):
    # Placeholder function to simulate loading of an MHD file
    # Replace with actual MHD file loading logic as needed
    return f"Loaded {file.name}"


def save_uploaded_file(uploaded_file):
    file_path = os.path.join('TempFiles', uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success(f"File {uploaded_file.name} saved successfully")



def ChoixClassification(methode, model):
    if methode == "GLCM":
        if model == "KNN":
            modele = joblib.load('models\GLCM_KNN.joblib')
        elif model == "SVM":
            modele = joblib.load('models\GLCM_SVM.joblib')
    elif methode == "Local binary patern":
        if model == "KNN":
            modele = joblib.load('models\LBP_KNN.joblib')
        elif model == "SVM":
            modele = joblib.load('models\LBP_SVM.joblib')
    elif methode == "Histogram of oriented gradients":
        if model == "KNN":
            modele = joblib.load('models\HOG_KNN++.joblib')
        elif model == "SVM":
            modele = joblib.load('models\HOG_SVM++.joblib')
    elif methode == "Gabor filter and HU":
        if model == "KNN":
            modele = joblib.load('models\Gabor_KNN.joblib')
        elif model == "SVM":
            modele = joblib.load('models\Gabor_SVM.joblib')
            
    return modele

def Prediction( choix, modele, chunk):
    if choix == "GLCM":
        features = GLCM(chunk)
        features = np.array(features).reshape(1, -1)
        result = modele.predict(features)
    elif choix == "Local binary patern":
        features = LBP(chunk)
        features = np.array(features).reshape(1, -1)
        result = modele.predict(features)
    elif choix == "Histogram of oriented gradients":
        features = HOG(chunk)
        features = np.array(features).reshape(1, -1)
        result = modele.predict(features)
    elif choix == "Gabor filter and HU":
        features = Gabor(chunk)
        features = np.array(features).reshape(1, -1)
        result = modele.predict(features)
        
    return result
    

