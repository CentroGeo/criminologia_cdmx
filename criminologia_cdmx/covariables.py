# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/api/02_covariables.ipynb.

# %% auto 0
__all__ = ['get_diccionario_censo', 'get_variables_censo', 'imputa_faltantes_manzana', 'agrega_en_unidades', 'censo_a_tasas',
           'get_uso_de_suelo', 'agrega_uso_suelo', 'IndicePCA']

# %% ../nbs/api/02_covariables.ipynb 3
import os
import glob
from pathlib import Path
from fastcore.basics import *
import numpy as np
import pandas as pd
import geopandas as gpd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from .etl import DATA_PATH, DOWNLOADS_PATH
import requests

# %% ../nbs/api/02_covariables.ipynb 5
def get_diccionario_censo() -> pd.DataFrame:
    """Regresa un DataFrame con el diccionario de variables del censo."""
    fname = 'diccionario_datos_ageb_urbana_09_cpv2020.csv'
    absp = os.path.abspath(os.path.join(DATA_PATH, fname))
    dicionario = pd.read_csv(absp, skiprows=3)
    diccionario = (dicionario
                   .drop(range(0,8))
                   .drop(columns='Núm.')
                   .reset_index(drop=True)
                   .rename({'Mnemónico':'Nombre del Campo'}, axis=1))
    return diccionario

# %% ../nbs/api/02_covariables.ipynb 8
def get_variables_censo() -> pd.DataFrame:
    """Regresa un DataFrame con las variables del censo a nivel manzana."""
    fname = 'censo_manzanas.zip'
    absp = os.path.abspath(os.path.join(DATA_PATH, fname))
    df = pd.read_csv(absp, dtype={'CVEGEO':str, 'colonia_cve': 'Int64'})
    return df

# %% ../nbs/api/02_covariables.ipynb 11
def imputa_faltantes_manzana(censo: pd.DataFrame, # Variables del censo en manzanas `get_variables_censo`,
                             cols: list, # Lista con las columnas en donde se deben imputar faltantes.
                             metodo:str='ceros' # método a usar para la imputación.
    ) -> pd.DataFrame: # Igual a `censo` pero con los datos faltantes imputados
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

# %% ../nbs/api/02_covariables.ipynb 15
def agrega_en_unidades(censo: pd.DataFrame, # Variables del censo en manzanas `get_variables_censo`
                       diccionario: pd.DataFrame, # `get_diccionario_censo`
                       agregacion:str='colonias', # colonias/cuadrantes o nombre del campo en `censo`
                       imputacion:str='ceros', # ceros/random. método para rellenar los datos faltantes.
                       umbral_faltantes:float=0.5  # Porcentaje de datos faltantes en una manzana para considerarla en el análisis
    ) -> pd.DataFrame: # Los datos del censo agregados en las unidades requeridas.
    """ Agrega las variables del censo en las unidades espaciales especificadas."""
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
    try:
        assert columna_agrega in censo.columns
    except AssertionError:
        print("La columna de agregación debe estar en los datos.")
        raise
    censo.dropna(thresh=umbral_faltantes*(len(vars_pob) + len(vars_viv)), inplace=True)
    censo = imputa_faltantes_manzana(censo, vars_pob + vars_viv, metodo=imputacion)
    censo = censo[[columna_agrega] + vars_pob + vars_viv].groupby(columna_agrega).sum()
    # Calculamos las columnas que requieren trato espacial
    censo['PROM_OCUP'] = censo['OCUPVIVPAR'].div(censo['VIVPAR_HAB'])
    censo['PROM_OCUP_C'] = censo['OCUPVIVPAR'].div(censo['VPH_1CUART'] + 2*censo['VPH_2CUART'] + 3*censo['VPH_3YMASC'])
    return censo

# %% ../nbs/api/02_covariables.ipynb 19
def censo_a_tasas(censo: pd.DataFrame, # Puede venir de `agrega_en_unidades` o `imputa_faltantes_manzana`
                  diccionario, # `get_diccionario_censo`
                  umbral_faltantes:float=0.5  # Porcentaje de datos faltantes en una manzana para considerarla en el análisis
    ):
    """ Convierte las variables del censo a tasas en la agregación seleccionada."""
    pob_col = 'POBTOT'
    hog_col = 'TOTHOG'
    viv_col = 'VIVPAR_HAB'
    vars_pob = [v for v in diccionario['Nombre del Campo'].unique() if v.startswith('P')]
    vars_pob_no_tasa = ['POBTOT', 'PROM_HNV']
    vars_pob = [v for v in vars_pob if (v not in vars_pob_no_tasa)]
    vars_viv_no_tasa = ['VIVPAR_HAB', 'PROM_OCUP', 'PRO_OCUP_C'] # No tiene sentido calcular tasas para estas variables
    vars_viv = [v for v in diccionario['Nombre del Campo'].unique() 
                if (v.startswith('V') and v not in vars_viv_no_tasa)]
    censo[vars_pob] = censo[vars_pob].div(censo[pob_col], axis=0)
    censo[vars_viv] = censo[vars_viv].div(censo[viv_col], axis=0)
    censo = censo.dropna(thresh=umbral_faltantes*(len(vars_pob) + len(vars_viv)))
    return censo

# %% ../nbs/api/02_covariables.ipynb 22
def get_uso_de_suelo() -> pd.DataFrame:
    """Regresa un DataFrame con las variables de uso de suelo a nivel manzana."""
    absp = os.path.abspath(os.path.join(DATA_PATH, 'usos_suelo.csv'))
    df = pd.read_csv(absp, dtype={'CVEGEO':str,'colonia_cve': 'Int64','cuadrante_id':str})
    return df

# %% ../nbs/api/02_covariables.ipynb 25
def agrega_uso_suelo(usos:pd.DataFrame, # `get_uso_de_suelo`
                     unidades:str='colonias' # colonias/cuadrantes
    ):
    """ Regresa un DataFrame con los usos agregados en las unidades espaciales."""
    if unidades == 'colonias':
        columna_agrega = 'colonia_cve'
    elif unidades == 'cuadrantes':
        columna_agrega = 'cuadrante_id'
    else:
        raise ValueError("unidades debe ser 'colonias' o 'cuadrantes'")
    usos = usos.groupby(columna_agrega).sum(numeric_only=True)
    usos['Intensidad'] = usos.sum(axis=1)
    usos['Entropía'] = (np.log(usos[['Industria', 'Comercio', 'Servicios']]
                               .div(usos['Intensidad'], axis=0))
                        .sum(axis=1) / np.log(3))
    return usos

# %% ../nbs/api/02_covariables.ipynb 28
class IndicePCA(object):
    """ Clase para crear indices basados en PCA."""
    def __init__(self, 
                covariables:pd.DataFrame, # `agrega_en_unidades` El índice del DataFrame debe ser el id de la unidad de agregación
                vars_indice:list # ista de las columnas con las que calculamos el índice
        ):
        self.datos = covariables
        self.vars_indice = vars_indice
        self.varianza_explicada = None
        self.indice = None
        


# %% ../nbs/api/02_covariables.ipynb 30
@patch
def calcula_indice(self:IndicePCA):
    """Calcula el índice y lo guarda en self.indice"""
    pca = PCA(n_components=1, svd_solver='full', random_state=1)
    indicadores = self.datos.replace([np.inf, -np.inf], np.nan)
    indicadores = indicadores[self.vars_indice].dropna()
    X = StandardScaler().fit_transform(indicadores.values)
    pca.fit(X)
    self.varianza_explicada = pca.explained_variance_ratio_
    indice = pca.fit_transform(X)[:,:1]
    id_var = indicadores.index.name
    df = indicadores.reset_index()[[id_var]]
    # df['Índice'] = abs(indice)
    df['Índice'] = indice
    self.indice = df
