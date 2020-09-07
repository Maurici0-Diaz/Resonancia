from itertools import product
import numpy as np
import xarray as xr

# Este archivo contiene las funciones xyz2grid y xyz2grd
# Los input deben ser tipo np.array()
# xyz2grid: toma como input vectores x, y, z , y los transforma a grillas (matrices) X,Y,Z.
# xyz2grd: pasa desde vectores x, y, z, los transforma a grillas X Y Z y guarda como dataset .grd

#funcion accum replica funcionamiento de accumarray en MATLAB.
#fuente: https://scipy-cookbook.readthedocs.io/items/AccumarrayLike.html

def accum(accmap, a, func=None, size=None, fill_value=0, dtype=None):
    """
    An accumulation function similar to Matlab's `accumarray` function.

    Parameters
    ----------
    accmap : ndarray
        This is the "accumulation map".  It maps input (i.e. indices into
        `a`) to their destination in the output array.  The first `a.ndim`
        dimensions of `accmap` must be the same as `a.shape`.  That is,
        `accmap.shape[:a.ndim]` must equal `a.shape`.  For example, if `a`
        has shape (15,4), then `accmap.shape[:2]` must equal (15,4).  In this
        case `accmap[i,j]` gives the index into the output array where
        element (i,j) of `a` is to be accumulated.  If the output is, say,
        a 2D, then `accmap` must have shape (15,4,2).  The value in the
        last dimension give indices into the output array. If the output is
        1D, then the shape of `accmap` can be either (15,4) or (15,4,1) 
    a : ndarray
        The input data to be accumulated.
    func : callable or None
        The accumulation function.  The function will be passed a list
        of values from `a` to be accumulated.
        If None, numpy.sum is assumed.
    size : ndarray or None
        The size of the output array.  If None, the size will be determined
        from `accmap`.
    fill_value : scalar
        The default value for elements of the output array. 
    dtype : numpy data type, or None
        The data type of the output array.  If None, the data type of
        `a` is used.

    Returns
    -------
    out : ndarray
        The accumulated results.

        The shape of `out` is `size` if `size` is given.  Otherwise the
        shape is determined by the (lexicographically) largest indices of
        the output found in `accmap`.


    Examples
    --------
    >>> from numpy import array, prod
    >>> a = array([[1,2,3],[4,-1,6],[-1,8,9]])
    >>> a
    array([[ 1,  2,  3],
           [ 4, -1,  6],
           [-1,  8,  9]])
    >>> # Sum the diagonals.
    >>> accmap = array([[0,1,2],[2,0,1],[1,2,0]])
    >>> s = accum(accmap, a)
    array([9, 7, 15])
    >>> # A 2D output, from sub-arrays with shapes and positions like this:
    >>> # [ (2,2) (2,1)]
    >>> # [ (1,2) (1,1)]
    >>> accmap = array([
            [[0,0],[0,0],[0,1]],
            [[0,0],[0,0],[0,1]],
            [[1,0],[1,0],[1,1]],
        ])
    >>> # Accumulate using a product.
    >>> accum(accmap, a, func=prod, dtype=float)
    array([[ -8.,  18.],
           [ -8.,   9.]])
    >>> # Same accmap, but create an array of lists of values.
    >>> accum(accmap, a, func=lambda x: x, dtype='O')
    array([[[1, 2, 4, -1], [3, 6]],
           [[-1, 8], [9]]], dtype=object)
    """

    # Check for bad arguments and handle the defaults.
    if accmap.shape[:a.ndim] != a.shape:
        raise ValueError("The initial dimensions of accmap must be the same as a.shape")
    if func is None:
        func = np.sum
    if dtype is None:
        dtype = a.dtype
    if accmap.shape == a.shape:
        accmap = np.expand_dims(accmap, -1)
    adims = tuple(range(a.ndim))
    if size is None:
        size = 1 + np.squeeze(np.apply_over_axes(np.max, accmap, axes=adims))
    size = np.atleast_1d(size)

    # Create an array of python lists of values.
    vals = np.empty(size, dtype='O')
    for s in product(*[range(k) for k in size]):
        vals[s] = []
    for s in product(*[range(k) for k in a.shape]):
        indx = tuple(accmap[s])
        val = a[s]
        vals[indx].append(val)

    # Create the output array.
    out = np.empty(size, dtype=dtype)
    for s in product(*[range(k) for k in size]):
        if vals[s] == []:
            out[s] = fill_value
        else:
            out[s] = func(vals[s])

    return out


# funcion xyz2grid transcripcion de xyz2grid.m en MATLAB
# los x,y,z de input tienen que ser tipo np.array()

#fuente:
# Author Info
# This script was written by Chad A. Greene of the University of Texas 
# at Austin's Institute for Geophysics (UTIG), April 2016. 
# http://www.chadagreene.com 

def xyz2grid(x,y,z):    # sintaxis para correr: X,Y,Z=xyz2grid(x,y,z)
    xs,xi=np.unique(x,return_inverse=True)
    ys,yi=np.unique(y,return_inverse=True)
    z=np.array(z)

    Z=accum(np.array(list(zip(yi,xi))), z,func=None,size=None,fill_value=np.nan,dtype=float)
    #Z=np.flipud(Z)
    X,Y=np.meshgrid(xs,ys)
    
    return X,Y,Z


def xyz2grd(x,y,z):         # sintaxis para correr: grd=xyz2grd(x,y,z)    
	X,Y,Z=xyz2grid(x,y,z)
	
	grd=xr.Dataset(
		{
			"z": (["y", "x"], Z)
		},
		coords={
			"x": ("x",X[0,:]),
			"y": ("y",Y[:,0]),

		},
	)
	
	return grd