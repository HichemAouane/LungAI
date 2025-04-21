# Classification des Nodules Pulmonaires via Analyse de Texture

Ce projet est issu d'un mémoire de fin d'études réalisé dans le cadre de la Licence en Informatique Académique à l'USTHB (Université des Sciences et de la Technologie Houari Boumediene).

## 🎯 Objectif du Projet

Le projet vise à améliorer la détection précoce du cancer du poumon en classifiant efficacement les nodules pulmonaires présents sur des images issues de CT Scans. L'approche principale consiste à exploiter différentes caractéristiques de la **texture** pour améliorer la classification des nodules, qu'ils soient bénins ou malins.

## 🧠 Méthodologie

Le projet repose sur deux grandes familles d'approches :

1. **Méthodes d'extraction de caractéristiques basées sur la texture :**
   - Local Binary Pattern (LBP)
   - Matrice de co-occurrence des niveaux de gris (GLCM) + Indices de Haralick
   - Histogramme des gradients orientés (HOG)
   - Filtre de Gabor
   - Moments de Hu

2. **Classification supervisée :**
   - K-Nearest Neighbors (KNN)
   - Support Vector Machines (SVM)
   - Réseaux de neurones convolutionnels (CNN) 3D

## 💾 Jeu de Données

Le projet utilise le dataset public **LUNA16** (LUng Nodule Analysis 2016), sous-ensemble du **LIDC-IDRI**, contenant des images CT annotées par des radiologues.

## ⚙️ Prétraitements

- Normalisation des images
- Redimensionnement des régions d'intérêt
- Augmentation de données
- Extraction de "chunks" contenant les nodules

## 🖼️ Interface Utilisateur

Une interface a été développée (avec **Streamlit**) permettant :
- de charger les CT Scans (`.mhd` / `.raw`),
- de spécifier les coordonnées des nodules,
- de sélectionner la méthode d'extraction des caractéristiques,
- de lancer la classification automatique.

## 🧪 Résultats

Les tests ont montré des taux de classification très prometteurs, avec des scores supérieurs à :
- 95% de précision sur les modèles basés sur **GLCM** et **LBP**.
- Améliorations constatées en combinant plusieurs approches.
- Le modèle **CNN 3D** a obtenu un score F1 très compétitif.

## 📂 Organisation du projet

📦 lung-nodule-texture-classification ├── data/ # Données CT Scans (prétraitées) 
├── notebooks/ # Jupyter Notebooks d'expérimentations 
├── src/ # Scripts Python 
├── models/ # Modèles entraînés 
├── app/ # Interface utilisateur Streamlit 
└── README.md

## 🛠️ Technologies utilisées

- Python
- NumPy, Pandas, Scikit-learn
- TensorFlow & Keras
- OpenCV, SimpleITK
- Streamlit pour l'application web

## 📜 Auteurs

- **Aouane Hichem**
- **Agrane Sabrina**  

Encadré par : **Dahmani Djamila**

Université : USTHB, Faculté Informatique — Algérie.

---

## 💡 Citation

Si vous utilisez ce travail, merci de citer :
Aouane, H., & Agrane, S. (2024). Une approche basée sur les caractéristiques de la texture pour la classification des nodules pulmonaires dans les images CT Scans. USTHB.

