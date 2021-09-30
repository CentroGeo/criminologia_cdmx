# AUTOGENERATED! DO NOT EDIT! File to edit: 01_patrones_espacio_temporales.ipynb (unless otherwise specified).

__all__ = ['ajusta_bandwidth_kde', 'kde2D']

# Cell
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
import numpy as np
import matplotlib.pyplot as plt
from .etl import *

# Cell
def ajusta_bandwidth_kde(x, y, bandwidth_space, xbins=100j, ybins=100j, **kwargs):
    """Regresa el valor de bandwidth con mejor log likelihood.

    Parametros:
    x, y: np.array con las coordenadas x y y de los puntos
    bandwith_space: np.linspace con el espacio de búsqueda
    xbins, ybins: complejos de numpy con el número de bins en x y y

    """

    # create grid of sample locations (default: 100x100)
    xx, yy = np.mgrid[x.min():x.max():xbins,
                      y.min():y.max():ybins]

    xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
    xy_train  = np.vstack([y, x]).T
    grid = GridSearchCV(KernelDensity(metric='haversine'), bandwidth_space)
    grid.fit(xy_train)
    return grid.best_estimator_.bandwidth

# Cell
def kde2D(x, y, bandwidth, xbins=100j, ybins=100j):
    """Regresa una matriz con la densidad de kernel para los puntos x,y.

    Parametros:
    x, y: np.array con las coordenadas x y y de los puntos
    bandwith: ancho del kernel gaussiano
    xbins, ybins: complejos de numpy con el número de bins en x y y

    """

    # create grid of sample locations (default: 100x100)
    xx, yy = np.mgrid[x.min():x.max():xbins,
                      y.min():y.max():ybins]

    xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
    xy_train  = np.vstack([y, x]).T

    kde_skl = KernelDensity(bandwidth=bandwidth, metric='haversine')
    kde_skl.fit(xy_train)

    # score_samples() returns the log-likelihood of the samples
    z = np.exp(kde_skl.score_samples(xy_sample))
    return xx, yy, np.reshape(z, xx.shape)