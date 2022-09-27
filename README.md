
criminologia_cdmx \> Preparar y ajustar modelos criminológicos para la
CDMX usando fácilmente diferentes fuentes de datos

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## Instalación

La forma más sencilla de instalarlo es creando un environment de conda
que tenga geopandas instalado y después usar `pip` para instalar la
librería dese el repositorio:

``` bash
conda create -n criminologia python=3.8
conda install -c conda-forge geopandas
pip install git+https://github.com/CentroGeo/criminologia_cdmx
```

Por lo pronto, como el repositorio es privado Git va a pedir usuario y
contraseña de GitHub.

Alternativamente, si tienes el repositorio clonado en la computadora:

``` bash
conda create -n criminologia python=3.8
conda install -c conda-forge geopandas
pip install git+file///ruta/a/criminologia_cdmx
```

## Uso

La librería provee, por lo pronto, cuatro módulos para trabajar con
datos sobre delincuencia en la CDMX, construir covariables y ajustar
modelos.

### etl

Este módulo descarga y transforma los datos básicos de delincuencia que
se pueden obtener de la página de [datos abiertos de la
CDMX](https://datos.cdmx.gob.mx/)

### hotspots

Aquí se encuentran diferentes algoritmos para hacer mapeo de hotspots.

### covariables

Analizar el crimen va más allá de ver los patrones espacio-temporales.
También queremos modelar estos patrones utilizando diferentes tipos de
covariables para entender cómo se relaciona la violencia criminal con,
por ejemplo, la marginación, la densidad de población o los usos de
suelo. Para hacer esto es necesario construir datos de estas
covariables, en este módulo vas a encintrar funciones que te ayudan a
hacer esto de forma sencilla a partir de diferentes fuentes de datos.

### modelos

Este módulo implementa diferentes tipos de modelos, espaciales y
aespaciales para asociar la violencia criminal con las variables
producidas en el módulo `covariables` (o también puedes usar facilmente
tus propias variables).

La documentación completa para cada módulo la puedes encontrar en el
menú de la izquierda en la sección `api`. También, en la sección de
`tutoriales` encontrarás ejemplos completos más desarrollados.
