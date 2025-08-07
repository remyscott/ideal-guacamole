import numpy as np

def normalize(vector):
    length = np.sqrt(vector[0]**2+vector[1]**2)
    return(vector/length)

def length(vector):
    length = np.sqrt(vector[0]**2+vector[1]**2)
    return(length)