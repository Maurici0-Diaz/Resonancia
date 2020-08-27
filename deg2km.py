import numpy as np

#funcion que transforma grados decimales a km
def deg2km(deg): # Input en grados
    
    rad=np.pi*deg/180 # Transforma a radianes
    radius=6371 #Radio promedio de la tierra (en km).
    km=radius*rad # Distancia en km
    
    return km