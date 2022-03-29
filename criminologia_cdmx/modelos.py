# AUTOGENERATED! DO NOT EDIT! File to edit: 03_modelos.ipynb (unless otherwise specified).

__all__ = ['variable_independiente', 'CapaDeAnalisis', 'ModeloGLM']

# Cell
import numpy as np
import pandas as pd
import geopandas as gpd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from .etl import *
from .covariables import *

# Cell
def variable_independiente(datos, columna_y, valor_y, fecha_inicio, fecha_fin, agregacion='colonias'):
    """ Regresa un DataFrame con la variable independicente agregada entre fecha_inicio y fecha_fin
        en las unidades requeridas.

        Args:
            datos (DataFrame): carpetas/victimas con ids espaciales y categorías de usuario
            columna_y (str): Nombre de la columna en donde vienen los incidentes de valor_y
            valor_y (str): delito o categoría a utilizar como Y
            fecha_inicio (str): fecha inicial para agregar delitos "d-m-Y"
            fecha_fin (str): fecha final para agregar delitos "d-m-Y"
            agregacion (str): colonias/cuadrantes. Eventualmente debe recibir
                              agregaciones arbitrarias
    """
    fecha_inicio = pd.to_datetime(fecha_inicio, dayfirst=True)
    fecha_fin = pd.to_datetime(fecha_fin, dayfirst=True)
    datos = datos.loc[datos['fecha_hechos'].between(fecha_inicio, fecha_fin)]
    datos = datos.loc[datos[columna_y] == valor_y]
    if agregacion == 'colonias':
        columna_agrega = 'colonia_cve'
        layer = 'colonias'
    elif agregacion == 'cuadrantes':
        columna_agrega = 'cuadrante_id'
        layer = 'cuadrantes'
    else:
        raise ValueError("unidades debe ser 'colonias' o 'cuadrantes'")
    datos = datos.groupby(columna_agrega).size()
    datos.name = valor_y
    unidades = gpd.read_file("datos/criminologia_capas.gpkg", layer=layer)
    datos = unidades[[columna_agrega]].merge(datos, on=columna_agrega, how='left').fillna(0)
    return datos

# Cell
class CapaDeAnalisis(object):
    """ Clase para contener variable objetivo y covariables.

        Args:
            Y (DataFrame): debe tener dos columnas: el identificador de la unidad de análisis y
                           el valor de la variable dependiente
                           (las columnas deben venir en ese orden).
            covariables (DataFrame): debe contener una columna con el identificador de la unidad
                                     de análisis (común a Y) y tantas como covariables.
            campo_id (str): el nombre del campo común en X y Y para unirlos.
        Atributos:
            Y (DataFrame): la variable dependiente.
            Y_nombre (str): Nombre de la columna con el delito a modelar.
            X (DataFrame): las variables independientes.
            X_nombres (list): Lista de los nombres de columnas de las covariables.
            campo_id (str): el nombre del campo común en X y Y para unirlos.
            df (DataFrame): la unión de los dos anteriores.
    """

    def __init__(self, Y, covariables, campo_id):
        self.Y = Y
        self.Y_nombre = Y.columns[-1]
        self.X = covariables
        self.X_nombres = [x for x in covariables.columns if x != campo_id]
        self.campo_id = campo_id
        self.df = self.__merge_covars()

    def __merge_covars(self):
        df = (self.Y.merge(self.X, on=self.campo_id)
                    .replace([np.inf, -np.inf], np.nan)
                    .dropna())
        return df

    # TODO:
    # agregar/quitar variables
    # checar que exista el campo_id en las dos bases
    # quitamos unas filas, hay que llevar registro de eso
    # Calcular variables con retraso espacial


# Cell
class ModeloGLM(object):
    """ Wrapper para modelos de Regresión GLM de statsmodels.

        La clase prepara y ajusta un modelo GLM usando la variable objetivo
        definida en CapaDeAnalisis y **todas** las covariables.

        Args:
            capa (CapaDeAnalisis): objeto con las variables del modelo.
            familia (statsmodels.api.families.Family()) la distribución a usar en el modelo GLM.
    """
    def __init__(self, capa, familia):
        self.capa = capa
        self.familia = familia
        self.formula = self.__get_formula()
        self.__modelo = self.__get_modelo()

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

    def fit(self):
        fm = self.__modelo.fit()
        return fm