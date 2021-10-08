# AUTOGENERATED! DO NOT EDIT! File to edit: 00_etl.ipynb (unless otherwise specified).

__all__ = ['get_carpetas_from_api', 'get_historico_carpetas', 'get_carpetas_desde_archivo', 'agrega_ids_espaciales',
           'agregar_categorias_de_usuario', 'exporta_datos_vusualizador', 'serie_de_tiempo_categoria']

# Cell
import os
import glob
import itertools
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from datetime import timedelta, date, datetime
import seaborn as sns
import requests

# Cell
def get_carpetas_from_api(limit=100):
    """Regresa un GeoDataFrame con los primeros `limit` registros de la base abierta."""
    url = f'https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=48fcb848-220c-4af0-839b-4fd8ac812c0f&limit={limit}'
    r = requests.get(url, allow_redirects=True)
    records = r.json()['result']['records']
    records = pd.DataFrame(records)
    records.replace('NA', np.nan, inplace=True)
    records.dropna(subset=['longitud', 'latitud'], how='any', inplace=True)
    records = gpd.GeoDataFrame(records, geometry=gpd.points_from_xy(records.longitud, records.latitud))
    records = records.set_crs(epsg=4326)
    records['fecha_hechos'] = pd.to_datetime(records.fecha_hechos)
    return records

# Cell
def get_historico_carpetas():
    """Regresa un GeoDataFrame con todos los registros de carpetas de investigación."""
    archivo = "datos/descargas/carpetas_fiscalia.csv"
    url = "https://archivo.datos.cdmx.gob.mx/fiscalia-general-de-justicia/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico/carpetas_completa_julio_2021.csv"
    r = requests.get(url, allow_redirects=True)
    open(archivo, 'wb').write(r.content)
    records = pd.read_csv(archivo)
    records.replace('NA', np.nan, inplace=True)
    records.dropna(subset=['longitud', 'latitud'], how='any', inplace=True)
    records = gpd.GeoDataFrame(records, geometry=gpd.points_from_xy(records.longitud, records.latitud))
    records = records.set_crs(epsg=4326)
    records['fecha_hechos'] = pd.to_datetime(records.fecha_hechos)
    return records

# Cell
def get_carpetas_desde_archivo(archivo):
    """Regresa un GeoDataFrame con los registros leídos de un archivo"""
    records = pd.read_csv(archivo)
    records.replace('NA', np.nan, inplace=True)
    records.dropna(subset=['longitud', 'latitud'], how='any', inplace=True)
    records = gpd.GeoDataFrame(records, geometry=gpd.points_from_xy(records.longitud, records.latitud))
    records = records.set_crs(epsg=4326)
    records['fecha_hechos'] = pd.to_datetime(records.fecha_hechos)
    return records

# Cell
def agrega_ids_espaciales(carpetas):
    """Agrega ids de colonias y cuadrantes a la base de carpetas."""
    colonias = gpd.read_file("datos/criminologia_capas.gpkg", layer='colonias').drop(columns='colonia_geom_6362')
    cuadrantes = gpd.read_file("datos/criminologia_capas.gpkg", layer='cuadrantes')
    carpetas = (gpd.tools.sjoin(carpetas, colonias[['colonia_cve', 'colonia_nombre', 'municipio_cvegeo', 'geometry']])
                .drop(columns=['index_right'])
               )
    carpetas = (gpd.tools.sjoin(carpetas, cuadrantes[['cuadrante_id', 'geometry']])
                .drop(columns=['index_right']))
    return carpetas

# Cell
def agregar_categorias_de_usuario(carpetas, archivo_categorias="datos/categorias_incidentes.csv"):
    """Agrega una columna con categorías definidas por el usuario.

      Las categorías tienen que venir en un csv con columnas incidente y categoria que
      relacionen las categorías del usuario con la columna delitos de la base de carpetas.
    """
    if 'categoria' in carpetas.columns:
        carpetas = carpetas.drop(columns='categoria')
    if 'incidente' in carpetas.columns:
        carpetas = carpetas.drop(columns='incidente')
    categorias = pd.read_csv(archivo_categorias)
    carpetas = (carpetas
                .merge(categorias, left_on='delito', right_on='incidente', how='left')
                .drop(columns='incidente'))
    return carpetas

# Cell
def exporta_datos_vusualizador(carpetas, archivo_resultado):
    """ Escribe en archivo_resultado un csv para consumirse en el visualizador."""
    carpetas['lat'] = carpetas.geometry.y
    carpetas['long'] = carpetas.geometry.x
    carpetas = carpetas[['fecha_hechos', 'delito', 'categoria', 'municipio_cvegeo', 'colonia_cve',
                         'cuadrante_id', 'categoria', 'lat', 'long']]
    carpetas.to_csv(archivo_resultado)

# Cell
def serie_de_tiempo_categoria(carpetas, fecha_inicio, categoria, freq='M'):
    """ Regresa una serie de tiempo con los agregados por `freq` de la `categoria`.

        parameters:
        carpetas: incidentes, deben traer la columna categoria
        fecha_inicio: pd.datetime fecha del inicio de la serie
        categoria: nombre de la categoría a agregar (`agregar_categorias_de_usuario`)
        freq: frecuencia de agregación (https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases)
    """
    carpetas = carpetas.loc[carpetas.fecha_hechos >= fecha_inicio]
    carpetas = carpetas.loc[carpetas.categoria == categoria]
    serie = (carpetas
             .set_index('fecha_hechos')[['categoria']]
             .resample(freq)
             .size()
             .reset_index()
             .rename({0:categoria}, axis=1)
            )
    return serie