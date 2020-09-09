import numpy as np
import pandas as pd

# los x,y,z de input tienen que ser tipo np.array()
# sintaxis para correr: X,Y,Z=xyz2grd(x,y,z)

def xyz2grid(x,y,z):

    df= pd.DataFrame(np.column_stack((x,y,z)), columns=['x', 'y', 'z'])
    df_grid=df.pivot(index='y',columns='x',values='z')

    xu=df_grid.columns.values
    yu=df_grid.index.values
    
    X,Y=np.meshgrid(xu,yu)
    
    Z=df_grid.values

    return X,Y,Z