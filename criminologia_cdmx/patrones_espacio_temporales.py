# AUTOGENERATED! DO NOT EDIT! File to edit: 01_patrones_espacio_temporales.ipynb (unless otherwise specified).

__all__ = ['construye_malla', 'ajusta_bandwidth_kde', 'kde2D', 'get_lista_datos', 'serie_tiempo_kde_categoria',
           'serie_razones_de_eventos', 'serie_mapas_intensidad', 'p_value_maps']

# Cell
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
import pandas as pd
import geopandas as gpd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from .etl import *
from functools import partial

# Cell
def construye_malla(datos, size):
    """ Regresa una malla (np.meshgrid) ajustada al extent de los datos,
        con el tamaño de celda especificado.

        Args:
            datos (GeoDataFrame): carpetas o víctimas
            size (float): tamaño de las celdas (en las unidades de la proyección)

    """
    xmin, ymin, xmax, ymax = datos.geometry.total_bounds
    xgrid = np.arange(xmin, xmax, size)
    ygrid = np.arange(ymin, ymax, size)
    X, Y = np.meshgrid(xgrid, ygrid)
    return (X, Y)

# Cell
def ajusta_bandwidth_kde(datos, bandwidth_space, size=1000,
                         malla=None, n_jobs=-1, metric="euclidean"):
    """ Regresa el valor de bandwidth con mejor log likelihood.

        Parametros:

            datos (GeoDataFrame):  víctimas o carpetas
            bandwith_space (np.linspace):  con el espacio de búsqueda
            size (float): Tamaño de la celda (en las unidades de la proyección).
                          Si se especifica malla se ignora
            malla (np.meshgrid): la malla en la que se va a ajustar el KDE, si es None se calcula
            n_jobs (int): número de procesos a usar (default = -1)
            metric (str): métrica a usar para calcular las distancias (default euclidean)
    """
    if malla is None:
        xx, yy = construye_malla(datos, size)
    else:
        xx = malla[0]
        yy = malla[1]
    xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
    x = datos.geometry.x.to_numpy()
    y = datos.geometry.y.to_numpy()
    xy_train  = np.vstack([y, x]).T
    grid = GridSearchCV(KernelDensity(metric=metric), bandwidth_space, n_jobs=n_jobs)
    grid.fit(xy_train)
    return grid.best_estimator_.bandwidth

# Cell

def kde2D(datos, bandwidth, size=1000, malla=None):
    """ Regresa una matriz con la densidad de kernel para los datos.

        Parametros:

            datos (GeoDataFrame):  víctimas o carpetas
            bandwith: ancho del kernel gaussiano
            size (float): Tamaño de la celda (en las unidades de la proyección).
                          Si se especifica malla se ignora
            metric (str): métrica a usar para calcular las distancias (default euclidean)
            malla (np.meshgrid): la malla en la que se va a ajustar el KDE, si es None se calcula
    """
    x = datos.geometry.x.to_numpy()
    y = datos.geometry.y.to_numpy()
    if malla is None:
        X, Y = construye_malla(datos, size)
    else:
        X = malla[0]
        Y = malla[1]
    XY = np.vstack([Y.ravel(), X.ravel()]).T
    xy_train = np.vstack([y, x]).T
    kde = KernelDensity(bandwidth=bandwidth)
    kde.fit(xy_train)
    # Z = kde.score_samples(XY)
    Z = np.exp(kde.score_samples(XY))
    return X, Y, np.reshape(Z, X.shape)

# Cell
def get_lista_datos(carpetas, fechas, categorias, offset):
    """ Regresa una lista de GeoDataFrames con los datos segmentados en fechas
        para la categoría seleccionada.

    """
    fecha_inicio = fechas[0] - pd.to_timedelta(offset)
    fechas.insert(0, fecha_inicio)
    intervalos = [(fechas[i-1], f) for i, f in enumerate(fechas[1:],1)]
    datos = []
    for intervalo in intervalos:
        datos_intervalo = carpetas.loc[(carpetas['fecha_hechos'].between(*intervalo, inclusive='left')) &
                                       (carpetas['categoria'].isin(categorias))]
        datos.append(datos_intervalo)
    return datos

# Cell
def serie_tiempo_kde_categoria(datos, size,
                               malla = None,
                               grid_search={'bandwidth': np.linspace(10, 10000, 100)},
                               bw=None):
    """ Ajusta kdes egregando los datos sobre cada categoria e intervalo de fecha.

       Args:
           datos list(GeoDataFrame): Lista con los datos para cada intervalo a procesar
           categorias: Lista de categorías para calcular el KDE
           offset: intervalo para agregar antes de la primera fecha, p.ej: "30 days" si los intervalos son mensuales
           size (float): Tamaño de la celda (en las unidades de la proyección)
           grid_search: {'bandwidth': np.linspace(0.001, 0.1, 100)} valores para ajustar el bandwidth (se usa sólo si bandwidth es nulo)
           bandwidth: Si no se especifica grid_search, se tiene que dar un valor de bandwidth
           **kwargs: argumentos extra que se pasan a `kde2D`

       returns:
       (xx, yy) [zz]: la tupla (xx, yy) es el grid común de los kdes, la lista contiene los valores de z para cada intervalo
    """
    if malla is None:
        malla = malla_comun(datos, size)
    if bw is None:
        bw = ajusta_bandwidth_kde(datos_intervalo, size, grid_search)
    kde2D_p = lambda d: kde2D(d, bw, size=size, malla=malla)
    kdes = map(kde2D_p, datos)
    kdes = [k[2] for k in kdes]
    return malla[0], malla[1], kdes

# Cell
def serie_razones_de_eventos(carpetas, fechas, categoria, offset, size, bw):
    """Regresa el mapa de razón entre una categoría con respecto a las demás."""
    datos_categoria = get_lista_datos(carpetas, fechas, categoria, offset)
    categorias_todas = list(carpetas[carpetas.categoria.notnull()]['categoria'].unique())
    categorias_todas = set(categorias_todas) - set(categoria)
    datos_base = get_lista_datos(carpetas, fechas, categorias_todas, offset)
    datos_completos = datos_categoria + datos_base
    malla = malla_comun(datos_completos, size)
    _, _, kdes_categoria = serie_tiempo_kde_categoria(datos_categoria, size, bw=bw, malla=malla)
    _, _, kdes_base = serie_tiempo_kde_categoria(datos_base, size, bw=bw, malla=malla)
    # TODO: vectorizar esta operación np.divide(a, b, out=np.zeros_like(a), where=b!=0)
    sr = [e / b for e,b in zip(kdes_categoria, kdes_base)]
    return malla[0], malla[1], sr

# Cell
def serie_mapas_intensidad(carpetas, fechas, categorias, offset, size, bw):
    """Regresa los mapas de razon y las intensidades de la categoría para las `fechas` seleccionadas."""
    xx, yy, razones = serie_razones_de_eventos(carpetas, fechas, categorias,
                                               offset, size, bw)
    avg = np.mean(razones, axis=0)
    std = np.std(razones, axis=0)
    intensidad = [(r - avg) / std for r in razones]
    p_values = []
    for r in razones:
        comp = [b >= r for b in razones]
        comp = np.sum(comp, axis=0)
        p = comp / (len(razones) + 1)
        p_values.append(p)
    return xx, yy, razones, intensidad, p_values

# Cell
def p_value_maps(razones):
    """Regresa los mapas de significancia estadística para las razones."""
    p_values = []
    for r in razones:
        comp = [b >= r for b in razones]
        comp = np.sum(comp, axis=0)
        p = comp / (len(razones) + 1)
        p_values.append(p)
    return p_values