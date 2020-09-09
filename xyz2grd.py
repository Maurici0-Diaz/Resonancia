import numpy as np
import xarray as xr
import pandas as pd

# los x,y,z de input tienen que ser tipo np.array()
# sintaxis para correr: X,Y,Z=xyz2grd(x,y,z)

def xyz2grd(x,y,z):

    df= pd.DataFrame(np.column_stack((x,y,z)), columns=['x', 'y', 'z'])
    df_grid=df.pivot(index='y',columns='x',values='z')

    xu=df_grid.columns.values
    yu=df_grid.index.values
    Z=df_grid.values

    grd=xr.Dataset(
            {
                "z": (["y", "x"], Z)
            },
            coords={
                "x": ("x",xu),
                "y": ("y",yu),
            },
        )

    return grd