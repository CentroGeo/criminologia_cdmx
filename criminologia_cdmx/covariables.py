# AUTOGENERATED! DO NOT EDIT! File to edit: 02_covariables.ipynb (unless otherwise specified).

__all__ = ['DATA_PATH', 'DOWNLOADS_PATH', 'descarga_datos_covariables', 'get_diccionario_censo', 'get_variables_censo',
           'imputa_faltantes_manzana', 'agrega_en_unidades', 'censo_a_tasas']

# Cell
import os
import glob
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import seaborn as sns
import requests

# Cell
DATA_PATH = "datos/"
DOWNLOADS_PATH = "datos/descargas/"

# Cell
def descarga_datos_covariables():
    """Descarga los archivos necesarios qe son demasiado grandes para el repositorio.

        - geometrías de manzanas
    """
    covariables_url = "https://www.dropbox.com/s/s49lb476wpwu2p1/covariables.gpkg?dl=1"
    r = requests.get(covariables_url, allow_redirects=True)
    open(DOWNLOADS_PATH + 'covariables.gpkg', 'wb').write(r.content)

# Cell
def get_diccionario_censo():
    """Regresa un DataFrame con el diccionario de variables del censo."""
    dicionario = pd.read_csv("datos/diccionario_datos_ageb_urbana_09_cpv2020.csv", skiprows=3)
    diccionario = (dicionario
                   .drop(range(0,8))
                   .drop(columns='Núm.')
                   .reset_index(drop=True)
                   .rename({'Mnemónico':'Nombre del Campo'}, axis=1))
    return diccionario

# Cell
def get_variables_censo():
    """Regresa un DataFrame con las variables del censo a nivel manzana."""
    df = pd.read_csv("datos/censo_manzanas.zip", dtype={'CVEGEO':str, 'colonia_cve': 'Int64'})
    return df

# Cell
def imputa_faltantes_manzana(censo, cols, metodo='ceros'):
    """ Regresa un df con los datos faltantes imputados a nivel manzana.

        params:

        cols: list: lista con las columnas en donde se deben imputar faltantes.
        metodo: método a usar para la imputación.
        NOTA: Por lo pronto sólo implementa dos métodos muy simples: llena con ceros
        o aleatorio entre 0 y 3. En el futuro podríamos implementar mejores formas
    """
    if metodo == 'ceros':
        censo = censo.fillna(0)
    elif metodo == 'random':
        rand = pd.DataFrame(np.random.randint(0, 4, size=(censo.shape[0], len(cols))),
                            columns=cols,
                            index=censo.index)
        censo.update(rand)
    else:
        raise ValueError("imputacion debe ser ceros o random")
    return censo

# Cell
def agrega_en_unidades(censo, diciconario,
                       agregacion        = 'colonias',
                       imputacion        = 'ceros',
                       umbral_faltantes  = 0.5):
    """ Agrega las variables del censo en las unidades espaciales especificadas.

        params:
        agregacion: str: colonias/cuadrantes o nombre del campo
        imputacion: str: ceros/random. método para rellenar los datos faltantes.
                             ceros llena con ceros, random con un aleatorio entre 0 y 3
                             (faltantes por secreto)
        umbral_faltantes float: Porcentaje de datos faltantes en una manzana para
                                considerarla en el análisis

        NOTA: La columna PROM_HNV se pierde porque no hay forma de calcularla.
    """
    vars_pob = [v for v in diccionario['Nombre del Campo'].unique()
                if (v.startswith('P') and v != 'PROM_HNV') ]
    vars_viv = [v for v in diccionario['Nombre del Campo'].unique() if v.startswith('V')]
    vars_viv.append('OCUPVIVPAR')
    if agregacion == 'colonias':
        columna_agrega = 'colonia_cve'
    elif agregacion == 'cuadrantes':
        columna_agrega = 'cuadrante_id'
    else:
        columna_agrega = agregacion
    assert columna_agrega in censo.columns
    censo.dropna(thresh=umbral_faltantes*(len(vars_pob) + len(vars_viv)), inplace=True)
    censo = imputa_faltantes_manzana(censo, vars_pob + vars_viv, metodo=imputacion)
    censo = censo[[columna_agrega] + vars_pob + vars_viv].groupby(columna_agrega).sum()
    censo['VPROM_OCUP'] = censo['OCUPVIVPAR'].div(censo['VIVPAR_HAB'])
    return censo

# Cell
def censo_a_tasas(censo, diccionario, agregacion='colonias', umbral_faltantes=0.5):
    """Convierte las variables del censo a tasas en la agregación seleccionada.

    Para las variables de población divide por población total.
    Para Hogares divide por TOTHOG.
    Para viviendas divide por el total de viviendas particulares
     habitadas (VIVPAR_HAB)

    params:
    umbral_faltantes float: Porcentaje de datos faltantes en una manzana para
    considerarla en el análisis
    """
    pob_col = 'POBTOT'
    hog_col = 'TOTHOG'
    viv_col = 'VIVPAR_HAB'
    vars_pob = [v for v in diccionario['Nombre del Campo'].unique() if v.startswith('P')]
    eliminar = ['POBTOT', 'PROM_HNV']
    vars_pob = [v for v in vars_pob if (v not in eliminar)]
    censo.dropna(thresh=umbral_faltantes*len(vars_pob), inplace=True)
    if agregacion == None:
        censo[vars_pob] = censo[vars_pob].div(censo[pob_col], axis=0)
    return censo