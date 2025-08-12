import numpy as np

def magnitude(vector):
    vector_magnitude = np.sqrt(sum(component**2 for component in vector))
    return(vector_magnitude)

def normalize(vector):
    vector_length = magnitude(vector)
    return(vector/vector_length)
