import copy
import time
from tqdm.notebook import tqdm
from collections import namedtuple
from fuctions import *
import joblib
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


def genfile(file, X, Y, Z):
    mhd_file = sitk.ReadImage(file)
    ct_scan = np.array(sitk.GetArrayFromImage(mhd_file), dtype=np.float32)
    ct_scan.clip(-1000, 1000, ct_scan)
    
    origin_xyz = mhd_file.GetOrigin()
    voxel_size_xyz = mhd_file.GetSpacing()
    direction_matrix = np.array(mhd_file.GetDirection()).reshape(3, 3)
    origin_xyz_np = np.array(origin_xyz)
    voxel_size_xyz_np = np.array(voxel_size_xyz)

    center_xyz = (X,Y,Z)
    cri = ((center_xyz - origin_xyz_np) @ np.linalg.inv(direction_matrix)) / voxel_size_xyz_np

# Since we'll be using column, row and index values to index into arrays,
# we round them to the nearest integer.
    cri = np.round(cri)

# Going forward, we'll need the scan to be in the order index, row, column
    irc = (int(cri[2]), int(cri[1]), int(cri[0]))
    
    dims_irc = (10, 18, 18)
    
    slice_list = []

    for axis, center_val in enumerate(irc):
    
    # Get start and end index for the dimension so that the
    # nodule center is at the center of the 3d array we extract
        start_index = int(round(center_val - dims_irc[axis]/2))
        end_index = int(start_index + dims_irc[axis])

    # Adjust the indexes if the start_index is out of the CT scan array
        if start_index < 0:
            start_index = 0
            end_index = int(dims_irc[axis])
    
        # Do the same check for the end_index
        if end_index > ct_scan.shape[axis]:
            end_index = ct_scan.shape[axis]
            start_index = int(ct_scan.shape[axis] - dims_irc[axis])
        
        slice_list.append(slice(start_index, end_index))
    
    tuple(slice_list)
    ct_scan_chunk = ct_scan[tuple(slice_list)]
    ct_scan_chunk.shape
    ctt = np.array(ct_scan_chunk).astype(int)
    max = np.max(ctt)
    min_val = np.min(ctt)
    max_val = np.max(ctt)

    # Normaliser le tableau à la plage [0, 255]
    nctt = (ctt - min_val) * (255 / (max_val+0.0000001 - min_val))

    # Convertir le tableau en type entier
    nctt = nctt.astype(np.uint8)
    return nctt
#la variable file doit contenir le path du fichier .mhd

#------------------------------------------------------------------------------------------------------------------
def GLCM(nctt):
    
    glcm_3d = np.zeros((256, 256, 1, 4))

    # Calculer la GLCM pour chaque plan de coupe (slice) de l'image 3D
    for z in range(nctt.shape[0]):
        glcm_slice = graycomatrix(nctt[z,:,:],[1], [0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)
        glcm_3d += glcm_slice
    
    glcm_sum = np.sum(glcm_3d)

    # Normaliser la matrice GLCM 3D
    glcm_3d_normalized = glcm_3d / glcm_sum
    
    GLCM_Energy = graycoprops(glcm_3d_normalized, 'energy')[0].mean()
    GLCM_corr = graycoprops(glcm_3d_normalized, 'correlation')[0].mean()
    GLCM_diss = graycoprops(glcm_3d_normalized, 'dissimilarity')[0].mean()
    GLCM_hom = graycoprops(glcm_3d_normalized, 'homogeneity')[0].mean()
    GLCM_contr = graycoprops(glcm_3d_normalized, 'contrast')[0].mean()
    
    return GLCM_Energy, GLCM_corr, GLCM_diss,GLCM_hom, GLCM_contr


#------------------------------------------------------------------------------------------------------------------------------

def LBP(nctt):
    
    lbp_3d = np.zeros((10, 18, 18))

    # Calculer la GLCM pour chaque plan de coupe (slice) de l'image 3D
    for z in range(nctt.shape[0]):
        lbp_slice = apply_lbp_image(nctt[z,:,:])
        lbp_3d += lbp_slice

    hist = calculate_lbp_histogram(lbp_3d)

    
    return hist
#-------------------------------------------------------------------------------------------------------------------------------------------------------

def HOG(nctt):
    ppcr = 8
    ppcc = 8
    hog_images = []
    hog_features = []
    hog_image_3d = np.zeros((10, 18, 18))
    fd_3d = np.zeros((10,32))
    blur = cv.GaussianBlur(nctt,(5,5),0)
    for z in range(blur.shape[0]):
        fd,hog_image = hog(blur[z,:,:], orientations=8, pixels_per_cell=(ppcr,ppcc),cells_per_block=(2,2),block_norm= 'L2',visualize=True)
        fd_3d[z,:] += fd 
        
    fd_3d = fd_3d.flatten()
    fd_3d = np.vstack(fd_3d)
    return fd_3d


#-----------------------------------------------------------------------------------------------------------------------------------------------

def Gabor(nctt):
    Gabor_image_3d = np.zeros((10, 18, 18))
    Hu_sum = np.zeros(7)
    for z in range(nctt.shape[0]):
        image = Gabor_process(nctt[z,:,:])
        Gabor_image_3d[z,:,:] += image
        features = calculerHu(image)
        Hu_sum += features[:,0]
    
    Hu_mean = Hu_sum / nctt.shape[0]
    

    
    return Hu_mean[0],Hu_mean[1],Hu_mean[2],Hu_mean[3],Hu_mean[4],Hu_mean[5],Hu_mean[6]


#-------------------------------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------

def genfileDL(file,X,Y,Z):
    mhd_file = sitk.ReadImage(file)
    ct_scan = np.array(sitk.GetArrayFromImage(mhd_file), dtype=np.float32)
    ct_scan.clip(-1000, 1000, ct_scan)
    origin_xyz = mhd_file.GetOrigin()
    voxel_size_xyz = mhd_file.GetSpacing()
    direction_matrix = np.array(mhd_file.GetDirection()).reshape(3, 3)
    origin_xyz_np = np.array(origin_xyz)
    voxel_size_xyz_np = np.array(voxel_size_xyz)

    center_xyz = (X,Y,Z)
    cri = ((center_xyz - origin_xyz_np) @ np.linalg.inv(direction_matrix)) / voxel_size_xyz_np

# Since we'll be using column, row and index values to index into arrays,
# we round them to the nearest integer.
    cri = np.round(cri)

# Going forward, we'll need the scan to be in the order index, row, column
    irc = (int(cri[2]), int(cri[1]), int(cri[0]))
    
    dims_irc = (32, 32, 32)
    
    slice_list = []

    for axis, center_val in enumerate(irc):
    
    # Get start and end index for the dimension so that the
    # nodule center is at the center of the 3d array we extract
        start_index = int(round(center_val - dims_irc[axis]/2))
        end_index = int(start_index + dims_irc[axis])

    # Adjust the indexes if the start_index is out of the CT scan array
        if start_index < 0:
            start_index = 0
            end_index = int(dims_irc[axis])
    
        # Do the same check for the end_index
        if end_index > ct_scan.shape[axis]:
            end_index = ct_scan.shape[axis]
            start_index = int(ct_scan.shape[axis] - dims_irc[axis])
        
        slice_list.append(slice(start_index, end_index))
    
    tuple(slice_list)
    ct_scan_chunk = ct_scan[tuple(slice_list)]
    ct_scan_chunk.shape
    ctt = np.array(ct_scan_chunk).astype(int)
    max = np.max(ctt)
    min_val = np.min(ctt)
    max_val = np.max(ctt)

    # Normaliser le tableau à la plage [0, 255]
    nctt = (ctt - min_val) * (255 / (max_val - min_val))
    nctt = nctt.astype(np.uint8)
    
    filename =  'chunk' 
    np.save( "TempFiles/" + filename + ".npy", nctt)
    return filename
    
    
#------------------------------------------------------------------------------------------------------------------
def Zoom(file,X,Y,Z):
    if os.path.exists('TempFiles/Zoom.png'):
        os.remove('TempFiles/Zoom.png')
    mhd_file = sitk.ReadImage(file)
    ct_scan = np.array(sitk.GetArrayFromImage(mhd_file), dtype=np.float32)
    ct_scan.clip(-1000, 1000, ct_scan)
    origin_xyz = mhd_file.GetOrigin()
    voxel_size_xyz = mhd_file.GetSpacing()
    direction_matrix = np.array(mhd_file.GetDirection()).reshape(3, 3)
    origin_xyz_np = np.array(origin_xyz)
    voxel_size_xyz_np = np.array(voxel_size_xyz)

    center_xyz = (X,Y,Z)
    cri = ((center_xyz - origin_xyz_np) @ np.linalg.inv(direction_matrix)) / voxel_size_xyz_np

# Since we'll be using column, row and index values to index into arrays,
# we round them to the nearest integer.
    cri = np.round(cri)

# Going forward, we'll need the scan to be in the order index, row, column
    irc = (int(cri[2]), int(cri[1]), int(cri[0]))
    
    dims_irc = (50, 50, 10)
    
    slice_list = []

    for axis, center_val in enumerate(irc):
    
    # Get start and end index for the dimension so that the
    # nodule center is at the center of the 3d array we extract
        start_index = int(round(center_val - dims_irc[axis]/2))
        end_index = int(start_index + dims_irc[axis])

    # Adjust the indexes if the start_index is out of the CT scan array
        if start_index < 0:
            start_index = 0
            end_index = int(dims_irc[axis])
    
        # Do the same check for the end_index
        if end_index > ct_scan.shape[axis]:
            end_index = ct_scan.shape[axis]
            start_index = int(ct_scan.shape[axis] - dims_irc[axis])
        
        slice_list.append(slice(start_index, end_index))
    
    tuple(slice_list)
    ct_scan_chunk = ct_scan[tuple(slice_list)]
    ct_scan_chunk.shape
    ctt = np.array(ct_scan_chunk).astype(int)
    max = np.max(ctt)
    min_val = np.min(ctt)
    max_val = np.max(ctt)

    # Normaliser le tableau à la plage [0, 255]
    nctt = (ctt - min_val) * (255 / (max_val - min_val))
    nctt = nctt.astype(np.uint8)
    
    plt.imshow(nctt[:,:,5], cmap='gray')
    plt.colorbar()  # Ajouter une barre de couleur
    plt.savefig('TempFiles/Zoom.png', format='png')