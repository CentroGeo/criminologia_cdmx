# AUTOGENERATED! DO NOT EDIT! File to edit: 00_etl.ipynb (unless otherwise specified).

__all__ = ['DATA_PATH', 'DOWNLOADS_PATH', 'get_carpetas_from_api', 'get_victimas_from_api', 'get_historico_carpetas',
           'get_historico_victimas', 'get_carpetas_desde_archivo', 'get_victimas_desde_archivo',
           'agrega_ids_espaciales', 'agregar_categorias_carpetas', 'agregar_categorias_victimas',
           'exporta_datos_visualizador', 'serie_de_tiempo_categoria', 'punto_to_hexid', 'agrega_en_hexagonos']

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
import h3
from shapely.geometry import Polygon

# Cell
DATA_PATH = "datos/"
DOWNLOADS_PATH = "datos/descargas/"

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
def get_victimas_from_api(limit=100):
    """Regresa un GeoDataFrame con los primeros `limit` registros de la base abierta de víctimas."""
    url = f'https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=d543a7b1-f8cb-439f-8a5c-e56c5479eeb5&limit={limit}'
    r = requests.get(url, allow_redirects=True)
    records = r.json()['result']['records']
    records = pd.DataFrame(records)
    records.replace('NA', np.nan, inplace=True)
    records.dropna(subset=['longitud', 'latitud'], how='any', inplace=True)
    records = gpd.GeoDataFrame(records, geometry=gpd.points_from_xy(records.longitud, records.latitud))
    records = records.set_crs(epsg=4326)
    records['FechaHecho'] = pd.to_datetime(records.FechaHecho)
    return records

# Cell
def get_historico_carpetas():
    """Regresa un GeoDataFrame con todos los registros de carpetas de investigación."""
    archivo = os.path.join(DOWNLOADS_PATH, 'carpetas_fiscalia.csv')
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
def get_historico_victimas():
    """Regresa un GeoDataFrame con todos los registros de victimas en carpetas de investigación."""
    archivo = os.path.join(DOWNLOADS_PATH, 'victimas_carpetas_fiscalia.csv')
    url = "https://archivo.datos.cdmx.gob.mx/fiscalia-general-de-justicia/victimas-en-carpetas-de-investigacion-fgj/victimas_completa_enero_2022.csv"
    r = requests.get(url, allow_redirects=True)
    open(archivo, 'wb').write(r.content)
    records = pd.read_csv(archivo)
    records.replace('NA', np.nan, inplace=True)
    records.dropna(subset=['longitud', 'latitud'], how='any', inplace=True)
    records = gpd.GeoDataFrame(records, geometry=gpd.points_from_xy(records.longitud, records.latitud))
    records = records.set_crs(epsg=4326)
    records['FechaHecho'] = pd.to_datetime(records.FechaHecho)
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
def get_victimas_desde_archivo(archivo):
    """Regresa un GeoDataFrame con los registros leídos de un archivo"""
    records = pd.read_csv(archivo)
    records.replace('NA', np.nan, inplace=True)
    records.dropna(subset=['longitud', 'latitud'], how='any', inplace=True)
    records = gpd.GeoDataFrame(records, geometry=gpd.points_from_xy(records.longitud, records.latitud))
    records = records.set_crs(epsg=4326)
    records['FechaHecho'] = pd.to_datetime(records.FechaHecho)
    return records

# Cell
def agrega_ids_espaciales(carpetas):
    """Agrega ids de colonias y cuadrantes a la base de carpetas."""
    shapes = os.path.join(DATA_PATH, 'criminologia_capas.gpkg')
    colonias = gpd.read_file(shapes, layer='colonias').drop(columns='colonia_geom_6362')
    cuadrantes = gpd.read_file(shapes, layer='cuadrantes')
    carpetas = (gpd.tools.sjoin(carpetas, colonias[['colonia_cve', 'colonia_nombre', 'municipio_cvegeo', 'geometry']])
                .drop(columns=['index_right'])
               )
    carpetas = (gpd.tools.sjoin(carpetas, cuadrantes[['cuadrante_id', 'geometry']])
                .drop(columns=['index_right']))
    return carpetas

# Cell
def agregar_categorias_carpetas(carpetas, archivo_categorias="datos/categorias_carpetas.csv"):
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
def agregar_categorias_victimas(carpetas, archivo_categorias="datos/categorias_victimas.csv"):
    """Columnas con niveles definidos por el usuario

      Las categorías tienen que venir en un csv con columnas llamadas Nivel 1, Nivel 2 ...
      que relacionen los niveles con las columnas Delito y Categoría en la base de Víctimas.
    """
    columnas_nivel = [c for c in carpetas.columns if 'Nivel' in c]
    if len(columnas_nivel):
        carpetas = carpetas.drop(columns=columnas_nivel)
    categorias = pd.read_csv(archivo_categorias)
    carpetas = (carpetas
                .merge(categorias, left_on='Delito', right_on='Delito', how='left')
                .drop(columns='Categoria_y')
                .rename({'Categoria_x': 'Categoria'}, axis=1)
                )
    return carpetas

# Cell
def exporta_datos_visualizador(carpetas, archivo_resultado, tipo='victimas'):
    """ Escribe en archivo_resultado un csv para consumirse en el visualizador.

        La opción tipo=victimas/carpetas controla si los datos de entrada son carpetas o victimas.
    """
    if tipo == 'carpetas':
        columnas = ['fecha_hechos', 'delito', 'categoria', 'municipio_cvegeo',
                    'colonia_cve', 'cuadrante_id', 'categoria', 'lat', 'long']
    elif tipo == 'victimas':
        columnas_nivel = [c for c in carpetas.columns if 'Nivel' in c]
        columnas = ['FechaHecho', 'Delito', 'Categoria', 'municipio_cvegeo',
                    'colonia_cve', 'cuadrante_id', 'lat', 'long'] + columnas_nivel
    carpetas['lat'] = carpetas.geometry.y
    carpetas['long'] = carpetas.geometry.x
    carpetas = carpetas[columnas]
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

# Cell
def punto_to_hexid(punto, resolution):
    """Regresa el hexid (h3) del punto."""
    return h3.geo_to_h3(punto.y, punto.x, resolution)

# Cell
def agrega_en_hexagonos(puntos, resolution):
    """Regresa un GeoDataFrame con las cuentas de puntos agregadas en hexágonos.

       params:
       puntos: GeoDataFrame: los puntos a agregar
       resolution: int: la resolución en uber.h3
    """
    puntos.loc[:,'hex_id'] = puntos.loc[:,'geometry'].apply(punto_to_hexid, args=[resolution])
    by_hex = puntos.groupby('hex_id').size().reset_index()
    # by_hex['geometry'] = by_hex['hex_id'].apply(lambda hex_id: Polygon(h3.h3_to_geo_boundary(hex_id)))
    by_hex['geometry'] = by_hex['hex_id'].apply(lambda hex_id: Polygon([x[::-1] for x in h3.h3_to_geo_boundary(hex_id)]))
    by_hex = gpd.GeoDataFrame(by_hex).rename({0:'incidentes'}, axis=1).set_crs(epsg=4326)
    return by_hex
