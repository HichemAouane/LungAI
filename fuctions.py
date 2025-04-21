import copy
import time
from tqdm.notebook import tqdm
from collections import namedtuple


import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import os
import glob
import SimpleITK as sitk
from PIL import Image
from imageio import imread

from PIL import Image
from imageio import imread
from joblib import Parallel, delayed
from collections import namedtuple
from skimage.feature import graycomatrix, graycoprops
from skimage.feature import hog
import cv2 as cv


def Gabor_filter(K_size=111, Sigma=7, Gamma=0.5, Lambda=np.pi, Psi=0, angle=0):
    # get half size
    d = K_size // 2

    # prepare kernel
    gabor = np.zeros((K_size, K_size), dtype=np.float32)

    # each value
    for y in range(K_size):
        for x in range(K_size):
            # distance from center
            px = x - d
            py = y - d

            # degree -> radian
            theta = angle / 180. * np.pi

            # get kernel x
            _x = np.cos(theta) * px + np.sin(theta) * py

            # get kernel y
            _y = -np.sin(theta) * px + np.cos(theta) * py

            # fill kernel
            gabor[y, x] = np.exp(-(_x**2 + Gamma**2 * _y**2) / (2 * Sigma**2)) * np.cos(2*np.pi*_x/Lambda + Psi)

    # kernel normalization
    gabor /= np.sum(np.abs(gabor))

    return gabor


# Use Gabor filter to act on the image
def Gabor_filtering(gray, K_size=111, Sigma=10, Gamma=1.2, Lambda=10, Psi=0, angle=0):
    # get shape
    H, W = gray.shape

    # padding
    gray = np.pad(gray, (K_size//2, K_size//2), 'edge')

    # prepare out image
    out = np.zeros((H, W), dtype=np.float32)

    # get gabor filter
    gabor = Gabor_filter(K_size=K_size, Sigma=Sigma, Gamma=Gamma, Lambda=Lambda, Psi=0, angle=angle)

    # filtering
    for y in range(H):
        for x in range(W):
            out[y, x] = np.sum(gray[y : y + K_size, x : x + K_size] * gabor)

    out = np.clip(out, 0, 255)
    out = out.astype(np.uint8)

    return out


# Use 6 Gabor filters with different angles to perform feature extraction on the image
def Gabor_process(img):
#     print(img.shape)
    # get shape
    H, W = img.shape

    # gray scale
    # gray = BGR2GRAY(img).astype(np.float32)

    # define angle
    #As = [0, 45, 90, 135]
    As = [0,30,60,90,120,150]

    # prepare pyplot
#     plt.subplots_adjust(left=0, right=1, top=1, bottom=0, hspace=0, wspace=0.2)

    out = np.zeros([H, W], dtype=np.float32)

    # each angle
    for i, A in enumerate(As):
    
        # gabor filtering
        _out = Gabor_filtering(img, K_size=11, Sigma=1.5, Gamma=1.2, Lambda=3, angle=A)
         

        # add gabor filtered image
        out += _out
        

    # scale normalization
    out = out /out.max()*255
    out = out.astype(np.uint8)

    return out

#2 fonctions que j'appelle pour la normalisation 
def copysign(x, y):
    """Return x with the sign of y."""
    return np.copysign(x, y)

def log10(x):
    """Return the base-10 logarithm of x."""
    return np.log10(x)

import cv2
from math import copysign, log10

def calculerHu(img):
    # seuiller l'image si <128 alors 0 si > alors 255 
    _,img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    
    # Calculer les moments de l'image
    moments = cv2.moments(img) 
    
    # Calculer les moments de Hu de l'image
    huMoments = cv2.HuMoments(moments)

    # Mise à l'échelle logarithmique des moments de Hu, normalisation et rendant les valeurs indépendantes de la rotation et de l'échelle
    for i in range(0, 7): 
        # moment_value = huMoments[i][0] if isinstance(huMoments[i], np.ndarray) else huMoments[i] // ligne au cas ou erreur
        huMoments[i] = (-1 * copysign(1.0, huMoments[i]) * log10(abs(huMoments[i] + 1e-10)))
    
    return huMoments


def assign_bit(picture, x, y, c):   
    bit = 0  
    try:          
        if picture[x][y] >= c: 
            bit = 1         
    except: 
        pass
    return bit 
#elle donne la valeur decimal d'une matrice apres LBP
def local_bin_val(picture, x, y):  
    eight_bit_binary = []
    centre = picture[x][y] 
    powers = [1, 2, 4, 8, 16, 32, 64, 128] 
    decimal_val = 0
    
    eight_bit_binary.append(assign_bit(picture, x-1, y + 1,centre)) 
    eight_bit_binary.append(assign_bit(picture, x, y + 1, centre)) 
    eight_bit_binary.append(assign_bit(picture, x + 1, y + 1, centre)) 
    eight_bit_binary.append(assign_bit(picture, x + 1, y, centre)) 
    eight_bit_binary.append(assign_bit(picture, x + 1, y-1, centre)) 
    eight_bit_binary.append(assign_bit(picture, x, y-1, centre)) 
    eight_bit_binary.append(assign_bit(picture, x-1, y-1, centre)) 
    eight_bit_binary.append(assign_bit(picture, x-1, y, centre))     
    
    for i in range(len(eight_bit_binary)): 
        decimal_val += eight_bit_binary[i] * powers[i] 
            
    return decimal_val 

#appliquer lbp sur une slice choisi et retourner la matrice LBP
def lbp_3d_from_mhd(s):
    lbp_slice = np.zeros_like(s, dtype=np.uint8)
    
    # Appliquer LBP sur chaque pixel 
    for i in range(s.shape[0]):
        for j in range(s.shape[1]):
            lbp_slice[i, j] = local_bin_val(s, i, j)
    
    return lbp_slice

def apply_lbp_image(slice):
    lbp_mat = lbp_3d_from_mhd(slice)  
    return lbp_mat
def calculate_lbp_histogram(image):
    hist, _ = np.histogram(image.ravel(), bins=np.arange(257), range=(0, 256))
    return hist

def flatten_array(arr):
    return arr.flatten()
