# AUTOGENERATED! DO NOT EDIT! File to edit: 03_modelos.ipynb (unless otherwise specified).

__all__ = ['variable_independiente', 'CapaDeAnalisis']

# Cell
import numpy as np
import pandas as pd
import geopandas as gpd
from .etl import *
from criminologia_cdmx. covariables import *

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
    """ Clase para contener varieble objetivo y covariables.

        Args:
            Y (DataFrame): debe tener dos columnas: el identificador de la unidad de análisis y
                           el valor de la variable dependiente.
            covariables (DataFrame): debe contener una columna con el identificador de la unidad
                                     de análisis (común a Y) y tantas como covariables.
        Atributos:
            Y (DataFrame): la variable dependiente
            X (DataFrame): las variables independientes
            df (DataFrame): la unión de los dos anteriores
    """

    def __init__(self, Y, covariables, campo_id):
        self.Y = Y
        self.X = covariables
        self.df = Y.merge(covariables, on=campo_id)
    # TODO:
    # agregar/quitar variables
    # checar que exista el campo_id en las dos bases
