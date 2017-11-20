from __future__ import division
import numpy as np
from matplotlib import image
from random import randint
from scipy.misc import logsumexp
from helper_functions import image_to_matrix, matrix_to_image, \
                             flatten_image_matrix, unflatten_image_matrix, \
                             image_difference

warnings.simplefilter(action="ignore", category=FutureWarning)


def k_means_cluster(image_values, k=3, initial_means=None):

    import random
    
    if image_values.ndim == 3:
        row,col,depth = image_values.shape
    else:
        row,col = image_values.shape
        depth = 1

    if initial_means == None:
        initial_means = np.zeros((k,depth))
        random_rows = random.sample(range(row),k)
        random_cols = random.sample(range(col),k)
        for count in range(k):
            initial_means[count] = image_values[random_rows[count]][random_cols[count]]
        
    distance =  np.zeros((k,row*col))
    image_values_flat = flatten_image_matrix(image_values)
    means = initial_means
    prev_cluster_allocation = np.zeros((1,row*col))
    
    while(1):
        for cluster_number in range(k):
            distance[cluster_number] = np.linalg.norm(image_values_flat - means[cluster_number],axis=1)

        cluster_allocation = np.argmin(distance, axis=0)
        if (np.array_equal(prev_cluster_allocation, cluster_allocation)):
            break;

        else:
            prev_cluster_allocation = cluster_allocation

        for cluster_number in range(k):
            indices = np.where(cluster_allocation == cluster_number)
            means[cluster_number] = np.mean(image_values_flat[[indices]][0],axis=0)
    
    for cluster_number in range(k):
        indices = np.where(cluster_allocation == cluster_number)
        image_values_flat[[indices]] = means[cluster_number]
        
    updated_image_values = unflatten_image_matrix(image_values_flat, col)
    return updated_image_values




updated_values = k_means_cluster(image_values, 10, initial_means = None)
matrix_to_image(updated_values, 'images/kmeans.png')
