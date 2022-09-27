# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/api/03_modelos.ipynb.

# %% auto 0
__all__ = ['variable_dependiente', 'CapaDeAnalisis', 'ModeloGLM', 'ComparaModelos']

# %% ../nbs/api/03_modelos.ipynb 3
import warnings
from functools import reduce
from itertools import chain
import math
import random
import string
import copy
import os
from fastcore.basics import patch
import numpy as np
import pandas as pd
import geopandas as gpd
from libpysal.weights import Queen, lag_spatial
from esda.moran import Moran
from splot.esda import moran_scatterplot
import statsmodels.formula.api as smf 
import statsmodels.api as sm
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from .etl import *
from .covariables import *

# %% ../nbs/api/03_modelos.ipynb 6
def variable_dependiente(datos:gpd.GeoDataFrame, # carpetas/victimas con ids espaciales y categorías de usuario
                         columna_y:str, # Nombre de la columna en donde vienen los incidentes de valor_y
                         valores_y:str, # delitos o categorías a utilizar como Y
                         fecha_inicio:str, # fecha inicial para agregar delitos "d-m-Y" 
                         fecha_fin:str, # fecha final para agregar delitos "d-m-Y"
                         agregacion:str='colonias', # colonias/cuadrantes/manzanas
                         nombre_y:str=None # Nombre para la columna con la variable dependiente
                         )->pd.DataFrame:
    """ Regresa un DataFrame con la variable independicente agregada entre fecha_inicio y fecha_fin
        en las unidades requeridas."""
    fecha_inicio = pd.to_datetime(fecha_inicio, dayfirst=True)
    fecha_fin = pd.to_datetime(fecha_fin, dayfirst=True)
    datos = datos.loc[datos['fecha_hechos'].between(fecha_inicio, fecha_fin)]
    datos = datos.loc[datos[columna_y].isin(valores_y)]
    if agregacion == 'colonias':
        columna_agrega = 'colonia_cve'
        layer = 'colonias'
    elif agregacion == 'cuadrantes':
        columna_agrega = 'cuadrante_id'
        layer = 'cuadrantes'
    elif agregacion == 'manzanas':
        try:
            assert 'manzana_cvegeo' in datos.columns
        except AssertionError:
            print("Para usar la agregación por manzanas primero \
                  debes agregar el identificador correspondiente")
            raise
        columna_agrega = 'manzana_cvegeo'
    else:
        raise ValueError("unidades debe ser 'colonias' o 'cuadrantes'")
    datos = datos.groupby(columna_agrega).size()
    if nombre_y is not None:
        datos.name = nombre_y
    else:
        datos.name = " ".join(valores_y)
    if agregacion in ('colonias', 'cuadrantes'):
        pth_capas = os.path.abspath(os.path.join(DATA_PATH, 'criminologia_capas.gpkg'))
        unidades = gpd.read_file(pth_capas, layer=layer)
    else:
        pth_manzanas = descarga_manzanas()
        unidades = (gpd
                    .read_file(pth_manzanas, layer="manzanas")
                    .rename({"CVEGEO": columna_agrega}, axis=1))
        
    datos = unidades[[columna_agrega]].merge(datos, on=columna_agrega, how='left').fillna(0)
    return datos   

# %% ../nbs/api/03_modelos.ipynb 10
class CapaDeAnalisis(object):
    """ Clase para contener variable objetivo y covariables."""
    
    def __init__(self,
                 Y:pd.DataFrame, # la variable dependiente.
                 covariables: pd.DataFrame, # las variables independientes
                 agregacion:str='colonias' # colonias/cuadrantes
                 ):
        self.Y:pd.DataFrame = Y # la variable dependiente.
        self.campo_id:str = self.__get_campo_id(agregacion) # el nombre del campo común en X y Y para unirlos.
        self.Y_nombre:str = Y.columns[-1] # Nombre de la columna con el delito a modelar. Se asume que la última columna tiene la variable de interés
        self.X:pd.DataFrame = covariables # las variables independientes
        self.X_nombres:list = [x for x in covariables.columns if x != self.campo_id] # Lista de los nombres de columnas de las covariables.
        self.agregacion:str = agregacion # colonias/cuadrantes
        self.df:pd.DataFrame = self.__merge_covars() # la unión de los X con Y.
        self.geo:gpd.GeoDataFrame = self.__get_geo(agregacion) # la unión de df con las geometrias que corresponden a `agregacion`
        self.w:Queen = self.__calcula_matriz_pesos() # Matriz de vecindad para los datos válidos
        # TODO self_repr() una función que describa en texto lo que pasó (datos válidos, etc.)
        
    def __merge_covars(self):
        """Regresa la unión de X y Y."""
        # TODO: aquí hay que contar cuántos datos perdimos por valores faltantes
        df = (self.Y.merge(self.X, on=self.campo_id)
                    .replace([np.inf, -np.inf], np.nan)
                    .dropna())
        df = df.set_index(self.campo_id)
        return df
    
    def __get_campo_id(self, agregacion):
        """ Regresa la columna que une los dataframes."""
        if agregacion == 'colonias':
            campo_id = 'colonia_cve'
        elif agregacion == 'cuadrantes':
            campo_id = 'cuadrante_id'
        else:
            raise ValueError("agregacion debe ser colonias o cuadrantes.")
        return campo_id
    
    def __get_geo(self, agregacion):
        """ Regresa el GeoDataframe correspondiente a la agregación."""
        geo = gpd.read_file(DATA_PATH/'criminologia_capas.gpkg', layer=agregacion)
        geo = geo.set_index(self.campo_id)
        geo = geo.join(self.df, how='inner')
        return geo
    
    def __calcula_matriz_pesos(self):
        """Regresa la matriz de peso y actualiza geo y df para eliminar las islas."""
        # TODO: aquí hay que contar los datos perdidos por islas
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            w = Queen.from_dataframe(self.geo.reset_index(), idVariable=self.campo_id)
            if len(w.islands):
                print(f"Las observaciones con {self.campo_id} {w.islands} son islas, las vamos a eliminar")
                self.df.drop(w.islands, inplace=True)
                self.geo.drop(w.islands, inplace=True)
                w = Queen.from_dataframe(self.geo)
        return w
    

        
    # TODO: 
    # agregar/quitar variables
    # checar que exista el campo_id en las dos bases
    # quitamos unas filas, hay que llevar registro de eso
    # Implementar transformadores sobre las variables
    

# %% ../nbs/api/03_modelos.ipynb 14
@patch
def copia(self:CapaDeAnalisis):
    """Regresa una copia del objeto"""
    return copy.deepcopy(self)

# %% ../nbs/api/03_modelos.ipynb 17
@patch
def displot_Y(self:CapaDeAnalisis, 
              size:tuple=(12,6) # Tamaño de la gráfica
            )->Axes:
    """Regresa el histograma de la variable dependiente."""
    f, ax = plt.subplots(1,figsize=size)
    ax = sns.histplot(data=self.Y, x=self.Y_nombre, ax=ax)
    ax.axvline(x=self.Y[self.Y_nombre].mean(), color='red')
    ax.set_ylabel("Conteo")
    return ax


# %% ../nbs/api/03_modelos.ipynb 23
@patch
def describe_Y(self:CapaDeAnalisis)->pd.DataFrame:
    """Regresa un DataFrame con estadísticas descriptivas de la variable dependiente."""
    d = self.Y[self.Y_nombre].describe()
    v = pd.Series({"Var":self.Y[self.Y_nombre].var()})
    d = pd.concat([d,v])
    d = pd.DataFrame(d)
    d = d.reset_index()
    d.columns = ['Estadístico', '']
    d = d.set_index('Estadístico')
    orden = ['count', 'mean','Var',  'std', 'min', '25%', '50%', '75%', 'max']
    d = d.reindex(orden)
    d = d.rename({'count': 'N', 'mean': 'Media', 
                    'Var':'Varianza', 
                    'std': 'Desviación estándar',
                    'min': 'Mínimo',
                    'max': 'Máximo'})
    return d

# %% ../nbs/api/03_modelos.ipynb 26
@patch
def retraso_x(self:CapaDeAnalisis, 
             columna # Sobre qué columna de `CapaDeAnalisis.X` vamos a calcular el retraso
    ) -> CapaDeAnalisis:
    """ Agrega una columna con el retraso espacial de la variable `columna`.
    
        La nueva columna se va a nombrar `columna`_lag.
        
        **NOTA:** Por lo pronto se usa la matriz de vecindad que calculada en 
        `__calcula_matriz_pesos`.
    """
    self.w.transform = 'R'
    rezago = lag_spatial(self.w, self.df[columna])
    self.df[columna + '_lag'] = rezago
    self.X_nombres.append(columna + '_lag')
    return self

# %% ../nbs/api/03_modelos.ipynb 29
@patch
def mapa_Y(self:CapaDeAnalisis,
           agregacion:str, # colonias/cuadrantes
           ax:Axes=None, # el eje en donde se hace el mapa
           size:tuple=(10,10), # tamaño del mapa (si se pasa un eje se ignora)
           clasificacion:str='quantiles', # squema de clasificación de mapclassify 
           cmap:str='YlOrRd', # mapa de colores de matplotlib 
           legend:bool=True # poner o no poner la leyenda
           ):
    """ Regresa un ax con el mapa de la variable dependiente."""
    capa = gpd.read_file("../../datos/criminologia_capas.gpkg", layer=agregacion)
    capa = capa.merge(self.Y, on=self.campo_id)
    if ax is None:
        f, ax = plt.subplots(1,figsize=size)
    ax = capa.plot(self.Y_nombre, scheme=clasificacion, ax=ax, cmap=cmap, legend=legend)
    ax.set_axis_off()
    ax.set_title(self.Y_nombre)
    return ax

# %% ../nbs/api/03_modelos.ipynb 32
@patch
def mapa_X(self:CapaDeAnalisis,
           covariable:str, # Nombre de la columna en X para hacer el mapa
           agregacion: str, # colonias/cuadrantes 
           ax:Axes=None, # el eje en donde se hace el mapa  
           size:tuple=(10,10), # tamaño del mapa 
           clasificacion:str='quantiles', # esquema de clasificación demapclassify
           cmap:str='YlOrRd', # mapa de colores de matplotlib
           legend:bool=True # poner o no poner la leyenda
           ):
    """ Regresa un ax con el mapa de la variable dependiente."""
    capa = gpd.read_file(DATA_PATH/"criminologia_capas.gpkg", layer=agregacion)
    capa = capa.merge(self.X, on=self.campo_id)
    if ax is None:
        f, ax = plt.subplots(1,figsize=size)
    ax = capa.plot(covariable, scheme=clasificacion, ax=ax, cmap=cmap, legend=legend)
    ax.set_axis_off()
    ax.set_title(covariable)
    return ax

# %% ../nbs/api/03_modelos.ipynb 35
class ModeloGLM(object):
    """ Wrapper para modelos de Regresión GLM de statsmodels."""
    def __init__(self,
                 capa:CapaDeAnalisis, # objeto con las variables del modelo. 
                 familia:sm.families.Family, # la distribución a usar en el modelo GLM.
                 nombre:str=None # Nombre para el modelo (si es None, se elige al azar)
        ):
        self.capa = capa
        self.familia = familia
        self.nombre = self.__get_nombre(nombre)
        self.formula:str = self.__get_formula() # la fórmula usada para ajustar el modelo.
        self.modelo = self.__get_modelo()
        self.modelo_ajustado = None
        self.df_resultado:pd.DataFrame = None # los resultados como DataFrame.
        self.df_diagnostico:pd.DataFrame = None #  los diagnósticos como DataFrame.
        self.gdf_residuales = None
        self.moran_p_residuales = None
        self.moran_dev_residuales = None

    def __get_nombre(self, nombre):
        if nombre is None:
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(5))
        else:
            return nombre
        
    def __get_formula(self):
        ls = f"Q('{self.capa.Y_nombre}') ~ "
        rs = ""
        for nombre in self.capa.X_nombres:
            rs += f"Q('{nombre}') + "        
        formula = ls + rs
        formula = formula[:-3]
        return formula
    
    def __get_modelo(self):
        modelo = smf.glm(formula = self.formula,
                         data    = self.capa.df, 
                         family  = self.familia)
        return modelo
    
    def __resultados_a_df(self, resultados):
        """LLena self.df_resultado con los resultados del ajuste."""
        results_df = pd.DataFrame({"coef":resultados.params,
                                   "std err": resultados.bse,
                                   "z": resultados.tvalues,
                                   "P>|z|":resultados.pvalues,
                                   "conf_lower":resultados.conf_int()[0],
                                   "conf_higher":resultados.conf_int()[1]
                                    })
        self.df_resultado = results_df

    def __diagnostico_a_df(self, resultados):
        """LLena self.df_diagnostico con los resultados del ajuste."""
        indice = ["Log-Likelihood", "Deviance", "Pearson chi2"]
        valores = [resultados.llf, resultados.deviance, resultados.pearson_chi2]
        results_df = pd.DataFrame({"Diagnóstico": indice, "Valor": valores})
        self.df_diagnostico = results_df
    
    def __residuales_gdf(self, resultados):
        """ Llena el campo gdf_residuales."""
        resid_dev = resultados.resid_deviance.copy()
        resid_dev = stats.zscore(resid_dev)
        resid_df = pd.DataFrame(resid_dev, columns=["Residual Deviance"])  
        resid_p = resultados.resid_pearson
        resid_p = pd.DataFrame(resid_p, columns=["Residual Pearson"])
        resid_df = resid_df.join(resid_p)
        mapa_residuales = self.capa.Y.join(resid_df, how='right')
        geos = (gpd.read_file(DATA_PATH/'criminologia_capas.gpkg',
                             layer=self.capa.agregacion)
                    .set_index(self.capa.campo_id))
        mapa_residuales = geos.join(mapa_residuales, how='right')
        self.gdf_residuales = mapa_residuales
        
    def __calcula_moran_residuales(self):
        moran_dev = Moran(self.gdf_residuales['Residual Deviance'].values, self.capa.w)
        self.moran_dev_residuales = moran_dev
        moran_p = Moran(self.gdf_residuales['Residual Pearson'].values, self.capa.w)
        self.moran_p_residuales = moran_p
        


# %% ../nbs/api/03_modelos.ipynb 41
@patch    
def fit(self:ModeloGLM):
        """ Ajusta el modelo y llena los campos correspondientes."""
        fm = self.modelo.fit()
        self.modelo_ajustado = fm
        self._ModeloGLM__resultados_a_df(fm)
        self._ModeloGLM__diagnostico_a_df(fm)
        self._ModeloGLM__residuales_gdf(fm)
        self._ModeloGLM__calcula_moran_residuales()
        return fm # La verdad creo que no es necesario regresar nada

# %% ../nbs/api/03_modelos.ipynb 49
@patch
def grafica_de_ajuste(self:ModeloGLM, 
                      size:tuple=(10,5), # Tamaño de la gráfica
                      ax:Axes=None # Eje para dibujar la gráfica 
    )-> Axes:
    """ Regresa un ax con la gráfica de ajuste del modelo."""
    if ax is None:
        f, ax = plt.subplots(1,figsize=size)
    y =  self.capa.df[self.capa.Y_nombre].values
    ax = sns.regplot(x=self.modelo_ajustado.mu, y=y, ax=ax)
    ax.set_title('Gráfica de Ajuste del Modelo')
    ax.set_ylabel('Valores observados')
    ax.set_xlabel('Valores ajustados')
    return ax

# %% ../nbs/api/03_modelos.ipynb 52
@patch
def grafica_residuales(self:ModeloGLM, 
                       tipo:str="deviance", # deviance/pearson 
                       size:tuple=(10,5), # Tamaño de la gráfica
                       ax:Axes=None # Eje para dibujar la gráfica
    )->Axes:
    """ Regresa un ax con la gráfica de Dependencia de los Residuales."""
    observados = self.capa.df[self.capa.Y_nombre].values
    if tipo == "deviance":
        y = self.modelo_ajustado.resid_deviance
        y_label = "Residual (Deviance)"
    else:
        y = self.modelo_ajustado.resid_pearson
        y_label = "Residual (Pearson)"
    if ax is None:
        f, ax = plt.subplots(1,figsize=size)
    ax = sns.scatterplot(x=observados, y=y, ax=ax)
    ax.hlines(0, 0, observados.max(), colors='black')
    ax.set_title('Gráfica de Dependencia de los Residuales')
    ax.set_ylabel(y_label)
    ax.set_xlabel('Valores ajustados')
    return ax  

# %% ../nbs/api/03_modelos.ipynb 55
@patch
def histograma_deviance(self:ModeloGLM,
                        size=(10,5), # Tamaño de la gráfica
                        ax=None # Eje para dibujar la gráfica
    )->Axes:
    """ Regresa un ax con el hitograma de deviance de los residuales."""
    resid = self.modelo_ajustado.resid_deviance.copy()
    resid_std = stats.zscore(resid)
    resid_std = pd.DataFrame(resid_std, columns=["Desviación"])
    if ax is None:
        f, ax = plt.subplots(1,figsize=size)
    ax = sns.histplot(data=resid_std, x="Desviación", ax=ax)
    ax.set_title('Histograma de desviación estandarizada')
    ax.set_ylabel('Conteo')
    return ax

# %% ../nbs/api/03_modelos.ipynb 58
@patch
def mapa_residuales(self:ModeloGLM,
                   tipo:str="deviance", # deviance/pearson 
                   size:tuple=(10,10), # tamaño del mapa
                   ax:Axes=None, # el eje en donde se hace el mapa
                   clasificacion:str='quantiles', # esquema de clasificación de mapclassify
                   cmap:str='YlOrRd', # mapa de colores de matplotlib 
                   legend:bool=True # poner o no poner la leyenda
    )-> Axes:
    """ Regresa un ax con el mapa de residuales (deviance/pearson)."""
    observados = self.capa.df[self.capa.Y_nombre].values
    if tipo == "deviance":
        y = self.modelo_ajustado.resid_deviance
        y_label = "Residual Deviance"
    else:
        y = self.modelo_ajustado.resid_pearson
        y_label = "Residual Pearson"
    if ax is None:
        f, ax = plt.subplots(1,figsize=size)
    ax = self.gdf_residuales.plot(y_label, 
                                    ax=ax, scheme=clasificacion, cmap=cmap, legend=legend)
    ax.set_axis_off()
    ax.set_title("Mapa de residuales")
    return ax

# %% ../nbs/api/03_modelos.ipynb 61
@patch
def scatterpĺot_moran(self:ModeloGLM, 
                      tipo:str="deviance", # deviance/pearson
                      ax=None # Eje en el que se grafica                
    )->Axes:
    """ Regresa un ax con el diagrama de dispersión de Moran para los residuales."""
    if tipo == "deviance":
        x_label = "Residual Deviance"
        moran = self.moran_dev_residuales
    elif tipo == "pearson":
        x_label = "Residual Pearson"
        moran = self.moran_p_residuales            
    else:
        raise ValueError("El tipo debe ser 'Residual Deviance' o 'Residual Pearson'")
    if ax is None:
        fig, ax = moran_scatterplot(moran, aspect_equal=True)
        ax.set_ylabel("Retraso espacial")
        ax.set_xlabel(x_label)
        ax.set_title(f"I de Moran {np.round(moran.I, 3)}, Significancia {moran.p_sim}")
    else:
        moran_scatterplot(moran, aspect_equal=True, ax=ax)
        ax.set_ylabel("Retraso espacial")
        ax.set_xlabel(x_label)
        ax.set_title(f"I de Moran {np.round(moran.I, 3)}, Significancia {moran.p_sim}")
    return ax

# %% ../nbs/api/03_modelos.ipynb 64
class ComparaModelos(object):
    """ Clase para construir comparaciones de modelos.
        Construte dos DataFrames para visualizar rápidamente una comparación de los modelos:
        uno con los resultados (coeficientes, etc) y otro con los diagnósticos.
        Args:
            modelos (list): Lista de modelos a comparar
            columnas (list): Lista de columnas que aparecen en la comparación de resultados 
                             (opcional, default None)
            redondeo: (int): Decimales a usar en la comparaciónn (opcional, default None)
        Atributos:
            modelos (list): Lista de modelos a comparar
            comparacion (DataFrame): comparación de los resultados
    """
    def __init__(self, modelos, columnas=None, redondeo=None):
        self.modelos = modelos
        self.comparacion = self.__une_resultados(columnas, redondeo)
        self.diagnosticos = self.__une_diagnosticos(redondeo)
    def __une_resultados(self, columnas, redondeo):
        if columnas is None:
            unidos = reduce(lambda left, right: 
                            left.df_resultado.join(right.df_resultado, 
                                                   how='outer', 
                                                   lsuffix="-" + left.nombre,
                                                   rsuffix="-" + right.nombre)
                            ,self.modelos)
        else:
            dfs = [(m.df_resultado, m.nombre) for m in self.modelos]
            dfs = [(df[0][columnas], df[1]) for df in dfs]
            unidos = reduce(lambda left, right: 
                            left[0].join(right[0], 
                                      how='outer', 
                                      lsuffix="-" + left[1],
                                      rsuffix="-" + right[1])
                            ,dfs)
            
        orden = [list(m.df_resultado.index) for m in self.modelos]
        orden = list(set().union(*orden))
        unidos = unidos.reindex(orden)
        if columnas is None:
            valores = self.modelos[0].df_resultado.columns
        else:
            valores = columnas
        nombres = ["Modelo " + m.nombre for m in self.modelos]
        indice_nuevo = pd.MultiIndex.from_product([nombres, valores])
        unidos.columns = indice_nuevo
        if redondeo:
            unidos = unidos.round(redondeo)
        return  unidos
    
    def __une_diagnosticos(self, redondeo):
        unidos = reduce(lambda left, right: 
                        left.df_diagnostico.merge(right.df_diagnostico, 
                                                  on="Diagnóstico",
                                                  suffixes=(" Modelo " + left.nombre, 
                                                            " Modelo " + right.nombre)),
                        self.modelos)
        if redondeo:
            unidos = unidos.round(redondeo)
        return unidos
        
    def graficas_de_ajuste(self, n_cols=2, size=(20,5)):
        """ Gráficas de ajuste para todos los modelos.
        
            Args:
            
                n_cols (int): Número de columnas en la figura
                size ((int, int)): Tamaño de la figura
        """
        n_modelos = len(self.modelos)
        filas = math.ceil(n_modelos / n_cols)
        f, axs = plt.subplots(filas, n_cols, figsize=size)
        f.suptitle('Gráficas de ajuste', fontsize=16)
        axs = axs.ravel()
        for i, ax in enumerate(axs):
            ax = self.modelos[i].grafica_de_ajuste(ax=ax)
            ax.set_title(f"{self.modelos[i].nombre}")
            
    def graficas_residuales(self, tipo='deviance', n_cols=2, size=(20,5)):
        """ Gráficas de residuales para todos los modelos.
        
        
            Args:
             
                tipo (str): pearson/deviance tipo de residuales a graficar.
                n_cols (int): Número de columnas en la figura.
                size ((int, int)): Tamaño de la figura.
        
        """
        n_modelos = len(self.modelos)
        filas = math.ceil(n_modelos / n_cols)
        f, axs = plt.subplots(filas, n_cols, figsize=size)
        f.suptitle('Gráficas de residuales', fontsize=16)        
        axs = axs.ravel()
        for i, ax in enumerate(axs):
            ax = self.modelos[i].grafica_residuales(tipo=tipo, ax=ax)
            ax.set_title(f"{self.modelos[i].nombre}")
            
    def histogramas_deviance(self, n_cols=2, size=(20,5)):
        """ Histogramas de deviance para todos los modelos.
        
            Args:
             
                n_cols (int): Número de columnas en la figura.
                size ((int, int)): Tamaño de la figura.        
        """
        
        n_modelos = len(self.modelos)
        filas = math.ceil(n_modelos / n_cols)
        f, axs = plt.subplots(filas, n_cols, figsize=size)
        f.suptitle('Histogramas de Deviance', fontsize=16)        
        axs = axs.ravel()
        for i, ax in enumerate(axs):
            ax = self.modelos[i].histograma_deviance(ax=ax)
            ax.set_title(f"{self.modelos[i].nombre}")
            
    def mapas_residuales(self, tipo='deviance', n_cols=2, 
                         size=(20,10), clasificacion='quantiles', 
                         cmap='YlOrRd', legend=True):
        """ Mapas de residuales para todos los modelos. 
        
        
            Args:
                
                tipo (str): deviance/pearson el tipo de residual a mapear
                n_cols (int): Número de columnas en la figura.
                size ((int, int)): Tamaño de la figura.
                clasificacion (str): esquema de clasificación (mapclassify).
                cmap (str): mapa de colores (matplotlib).
                legend (bool): desplegar o no la leyenda.
        """
        n_modelos = len(self.modelos)
        filas = math.ceil(n_modelos / n_cols)
        f, axs = plt.subplots(filas, n_cols, figsize=size)
        f.suptitle(f'Mapas de residuales de {tipo}', fontsize=16)        
        axs = axs.ravel()
        for i, ax in enumerate(axs):
            # TODO:size
            ax = self.modelos[i].mapa_residuales(tipo=tipo, ax=ax, 
                                                 clasificacion=clasificacion, 
                                                 cmap=cmap, legend=legend)
            ax.set_title(f"{self.modelos[i].nombre}")
            
    def scatterpĺots_moran(self, tipo="deviance", n_cols=2, size=(20,10)):
        """ Graficas de moran para todos los modelos.
        
        
            Args:
                
                tipo (str): deviance/pearson el tipo de residual a mapear
                n_cols (int): Número de columnas en la figura.
                size ((int, int)): Tamaño de la figura.
        """
        
        n_modelos = len(self.modelos)
        filas = math.ceil(n_modelos / n_cols)
        f, axs = plt.subplots(filas, n_cols, figsize=size)
        if tipo == "deviance":
            titulo = 'Residuales de Deviance'
        else:
            titulo = 'Residuales de Pearson'
        f.suptitle(titulo, fontsize=16)        
        axs = axs.ravel()
        for i, ax in enumerate(axs):
            ax = self.modelos[i].scatterpĺot_moran(tipo="deviance", ax=ax)
            if tipo == "deviance":
                moran = self.modelos[i].moran_dev_residuales
            else:
                moran = self.modelos[i].moran_p_residuales
            
            ax.set_title(f"Modelo {self.modelos[i].nombre}: I de Moran {np.round(moran.I, 3)}, Significancia {moran.p_sim}")
        plt.tight_layout()
