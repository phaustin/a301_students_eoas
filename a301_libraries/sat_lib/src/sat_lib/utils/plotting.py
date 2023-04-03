import copy
from matplotlib import cm
from matplotlib.colors import Normalize
def make_cmap(vmin, vmax, cmap = None,
              over = 'w',under='k',missing='0.4'):
    """
    return Normalization and colormap

    Parameters
    ----------

    vmin, vmax: float
       colormap max and min values
    cmap: cm.colormap
       optional, default - cm.viridis
    over,under,missing: str
       colors for data large, small, missing data
       defaults: over = 'w',under='k',missing='0.4'

    Returns
    -------

    the_norm:  Normalization for vmin and vmax
    cmap: colormap with over, under and missing 
    
    """
    if cmap is None:
        cmap = cm.viridis
    the_norm=Normalize(vmin=vmin,vmax=vmax,clip=False)
    cmap=copy.copy(cmap)
    cmap.set_over(over)
    cmap.set_under(under)
    cmap.set_bad(missing) # grey
    return the_norm, cmap
