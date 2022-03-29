# criminologia_cdmx
> Herramientas para el análisis espacial de la delincuencia en la CDMX.


## Instalación

La forma más sencilla de instalarlo es creando un environment de conda que tenga geopandas instalado y después usar `pip` para instalar la librería dese el repositorio:


````bash
conda create -n criminologia python=3.7
conda install -c conda-forge geopandas
pip install git+https://github.com/CentroGeo/criminologia_cdmx
````

Por lo pronto, como el repositorio es privado Git va a pedir usuario y contraseña de GitHub.

Alternativamente, si tienes el repositorio clonado en la computadora:

````bash
conda create -n criminologia python=3.7
conda install -c conda-forge geopandas
pip install git+file///ruta/a/criminologia_cdmx
````

## Uso

## ETL
````Python
from criminologia_cdmx.etl import *
````

### Bajar datos abiertos

Podemos bajar dos fuentes de datos: [carpetas de investigación](https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico) y [víctimas en carpetas de investigación](https://datos.cdmx.gob.mx/dataset/victimas-en-carpetas-de-investigacion-fgj/resource/d543a7b1-f8cb-439f-8a5c-e56c5479eeb5).

Hay dos formas de bajar los datos abiertos, la primera es usando el api que baja las primeras `limit` carpetas/víctimas de la base abierta

```python
carpetas = get_carpetas_from_api(limit=100)
carpetas.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>_id</th>
      <th>ao_hechos</th>
      <th>mes_hechos</th>
      <th>fecha_hechos</th>
      <th>ao_inicio</th>
      <th>mes_inicio</th>
      <th>fecha_inicio</th>
      <th>delito</th>
      <th>fiscalia</th>
      <th>agencia</th>
      <th>...</th>
      <th>categoria_delito</th>
      <th>calle_hechos</th>
      <th>calle_hechos2</th>
      <th>colonia_hechos</th>
      <th>alcaldia_hechos</th>
      <th>competencia</th>
      <th>longitud</th>
      <th>latitud</th>
      <th>tempo</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>751816</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07 14:00:00</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07T21:45:16</td>
      <td>PRODUCCIÓN, IMPRESIÓN, ENAJENACIÓN, DISTRIBUCI...</td>
      <td>INVESTIGACIÓN EN COYOACÁN</td>
      <td>COY-1</td>
      <td>...</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>MIGUEL ANGEL DE QUEVEDO</td>
      <td>NaN</td>
      <td>ROMERO DE TERREROS</td>
      <td>COYOACAN</td>
      <td>NaN</td>
      <td>-99.17525</td>
      <td>19.34586</td>
      <td>NaN</td>
      <td>POINT (-99.17525 19.34586)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>751817</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07 14:00:00</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07T21:46:30</td>
      <td>DAÑO EN PROPIEDAD AJENA CULPOSA POR TRÁNSITO V...</td>
      <td>INVESTIGACIÓN EN ÁLVARO OBREGÓN</td>
      <td>AO-4</td>
      <td>...</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>AVENIDA PERIFERICO SUR</td>
      <td>CALZADA LAS AGUILAS</td>
      <td>LOS ALPES</td>
      <td>ALVARO OBREGON</td>
      <td>NaN</td>
      <td>-99.19513</td>
      <td>19.35819</td>
      <td>NaN</td>
      <td>POINT (-99.19513 19.35819)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>751818</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-06 23:30:00</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07T21:49:20</td>
      <td>ROBO A TRANSEUNTE CONDUCTOR DE TAXI PUBLICO Y ...</td>
      <td>INVESTIGACIÓN EN IZTAPALAPA</td>
      <td>IZP-6</td>
      <td>...</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>AV. TELECOMUNICACIONES</td>
      <td>AV. GENERAL ANTONIO LEON LOYOLA (AMBAS SON PAR...</td>
      <td>UNIDAD EJÉRCITO CONSTITUCIONALISTA</td>
      <td>IZTAPALAPA</td>
      <td>NaN</td>
      <td>-99.04765</td>
      <td>19.38716</td>
      <td>NaN</td>
      <td>POINT (-99.04765 19.38716)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>751819</td>
      <td>2019</td>
      <td>Septiembre</td>
      <td>2019-09-14 12:00:00</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07T21:57:48</td>
      <td>FRAUDE</td>
      <td>INVESTIGACIÓN EN BENITO JUÁREZ</td>
      <td>BJ-3</td>
      <td>...</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>EUGENIA</td>
      <td>NaN</td>
      <td>NARVARTE</td>
      <td>BENITO JUAREZ</td>
      <td>NaN</td>
      <td>-99.16102</td>
      <td>19.38601</td>
      <td>NaN</td>
      <td>POINT (-99.16102 19.38601)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>751820</td>
      <td>2019</td>
      <td>Agosto</td>
      <td>2019-08-13 13:00:00</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07T21:59:40</td>
      <td>VIOLENCIA FAMILIAR</td>
      <td>JUZGADOS FAMILIARES</td>
      <td>CJM-TLP</td>
      <td>...</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>AVENIDA GUSTAVO DIAZ ORDAZ</td>
      <td>NaN</td>
      <td>AMPLIACIÓN JALALPA</td>
      <td>ALVARO OBREGON</td>
      <td>NaN</td>
      <td>-99.23382</td>
      <td>19.37586</td>
      <td>NaN</td>
      <td>POINT (-99.23382 19.37586)</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>



```python
victimas = get_victimas_from_api(limit=100)
victimas.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>_id</th>
      <th>idCarpeta</th>
      <th>Ano_inicio</th>
      <th>Mes_inicio</th>
      <th>FechaInicio</th>
      <th>delito</th>
      <th>categoria</th>
      <th>Sexo</th>
      <th>Edad</th>
      <th>TipoPersona</th>
      <th>...</th>
      <th>fecha_hechos</th>
      <th>HoraHecho</th>
      <th>HoraInicio</th>
      <th>AlcaldiaHechos</th>
      <th>ColoniaHechos</th>
      <th>Calle_hechos</th>
      <th>Calle_hechos2</th>
      <th>latitud</th>
      <th>longitud</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>595358</td>
      <td>8960172</td>
      <td>2021</td>
      <td>Junio</td>
      <td>2021-06-26T00:00:00</td>
      <td>ROBO DE VEHICULO DE SERVICIO PARTICULAR CON VI...</td>
      <td>ROBO DE VEHÍCULO CON Y SIN VIOLENCIA</td>
      <td>Masculino</td>
      <td>25</td>
      <td>FISICA</td>
      <td>...</td>
      <td>2021-06-26</td>
      <td>19:10:00</td>
      <td>22:17:00</td>
      <td>ALVARO OBREGON</td>
      <td>PUERTA GRANDE</td>
      <td>AVENIDA CENTENARIO   CASI ESQUINA CON LA CALLE...</td>
      <td>NaN</td>
      <td>19.3571148543388</td>
      <td>-99.2289503701792</td>
      <td>POINT (-99.22895 19.35711)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>595359</td>
      <td>8960173</td>
      <td>2021</td>
      <td>Junio</td>
      <td>2021-06-26T00:00:00</td>
      <td>ROBO A TRANSPORTISTA Y VEHICULO PESADO CON VIO...</td>
      <td>ROBO A TRANSPORTISTA CON Y SIN VIOLENCIA</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>MORAL</td>
      <td>...</td>
      <td>2021-06-25</td>
      <td>23:30:00</td>
      <td>22:17:00</td>
      <td>AZCAPOTZALCO</td>
      <td>INDUSTRIAL VALLEJO</td>
      <td>AVENIDA CEYLAN</td>
      <td>ENTRE CERRADA CEYLAN</td>
      <td>19.4938324187342</td>
      <td>-99.1699397596072</td>
      <td>POINT (-99.16994 19.49383)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>595360</td>
      <td>8960173</td>
      <td>2021</td>
      <td>Junio</td>
      <td>2021-06-26T00:00:00</td>
      <td>ROBO A TRANSPORTISTA Y VEHICULO PESADO CON VIO...</td>
      <td>ROBO A TRANSPORTISTA CON Y SIN VIOLENCIA</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>MORAL</td>
      <td>...</td>
      <td>2021-06-25</td>
      <td>23:30:00</td>
      <td>22:17:00</td>
      <td>AZCAPOTZALCO</td>
      <td>INDUSTRIAL VALLEJO</td>
      <td>AVENIDA CEYLAN</td>
      <td>ENTRE CERRADA CEYLAN</td>
      <td>19.4938324187342</td>
      <td>-99.1699397596072</td>
      <td>POINT (-99.16994 19.49383)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>595361</td>
      <td>8960175</td>
      <td>2021</td>
      <td>Junio</td>
      <td>2021-06-26T00:00:00</td>
      <td>ROBO A NEGOCIO SIN VIOLENCIA POR FARDEROS (TIE...</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>MORAL</td>
      <td>...</td>
      <td>2021-06-26</td>
      <td>21:20:00</td>
      <td>22:21:00</td>
      <td>IZTAPALAPA</td>
      <td>GUADALUPE DEL MORAL</td>
      <td>AVENIDA JAVIER ROJO GOMEZ</td>
      <td>NaN</td>
      <td>19.3681183577951</td>
      <td>-99.0814492098267</td>
      <td>POINT (-99.08145 19.36812)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>595362</td>
      <td>8960176</td>
      <td>2021</td>
      <td>Junio</td>
      <td>2021-06-26T00:00:00</td>
      <td>FRAUDE</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>Masculino</td>
      <td>37</td>
      <td>FISICA</td>
      <td>...</td>
      <td>2021-06-26</td>
      <td>08:27:00</td>
      <td>22:31:00</td>
      <td>BENITO JUAREZ</td>
      <td>NAPOLES</td>
      <td>ARIZONA</td>
      <td>PENSILVANIA</td>
      <td>19.3927810885787</td>
      <td>-99.1806440001974</td>
      <td>POINT (-99.18064 19.39278)</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 24 columns</p>
</div>



La segunda es bajar el histórico completo:

````Python
carpetas_todas = get_historico_carpetas()
victimas_todas = get_historico_victimas()
````

También es posible procesar los datos a partir de un archivo guardado en la computadora, ya sea obtenido de la página de datos abiertos o guardado con las funciones `get_historico_carpetas`/`get_historico_victimas`.

````Python
carpetas = get_carpetas_desde_archivo("path-a-los-datos")
victimas_todas = get_victimas_desde_archivo("path-a-los-datos")
````

### Agregar identificadores espaciales (carpetas o victimas)

Para agregar los identificadores de colonia y cuadrante:

```python
carpetas = agrega_ids_espaciales(carpetas)
carpetas.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>_id</th>
      <th>ao_hechos</th>
      <th>mes_hechos</th>
      <th>fecha_hechos</th>
      <th>ao_inicio</th>
      <th>mes_inicio</th>
      <th>fecha_inicio</th>
      <th>delito</th>
      <th>fiscalia</th>
      <th>agencia</th>
      <th>...</th>
      <th>alcaldia_hechos</th>
      <th>competencia</th>
      <th>longitud</th>
      <th>latitud</th>
      <th>tempo</th>
      <th>geometry</th>
      <th>colonia_cve</th>
      <th>colonia_nombre</th>
      <th>municipio_cvegeo</th>
      <th>cuadrante_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>751816</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07 14:00:00</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07T21:45:16</td>
      <td>PRODUCCIÓN, IMPRESIÓN, ENAJENACIÓN, DISTRIBUCI...</td>
      <td>INVESTIGACIÓN EN COYOACÁN</td>
      <td>COY-1</td>
      <td>...</td>
      <td>COYOACAN</td>
      <td>NaN</td>
      <td>-99.17525</td>
      <td>19.34586</td>
      <td>NaN</td>
      <td>POINT (-99.17525 19.34586)</td>
      <td>1149</td>
      <td>ROMERO DE TERREROS (FRACC)</td>
      <td>09003</td>
      <td>023</td>
    </tr>
    <tr>
      <th>1</th>
      <td>751817</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07 14:00:00</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07T21:46:30</td>
      <td>DAÑO EN PROPIEDAD AJENA CULPOSA POR TRÁNSITO V...</td>
      <td>INVESTIGACIÓN EN ÁLVARO OBREGÓN</td>
      <td>AO-4</td>
      <td>...</td>
      <td>ALVARO OBREGON</td>
      <td>NaN</td>
      <td>-99.19513</td>
      <td>19.35819</td>
      <td>NaN</td>
      <td>POINT (-99.19513 19.35819)</td>
      <td>264</td>
      <td>ALPES</td>
      <td>09010</td>
      <td>015</td>
    </tr>
    <tr>
      <th>2</th>
      <td>751818</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-06 23:30:00</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07T21:49:20</td>
      <td>ROBO A TRANSEUNTE CONDUCTOR DE TAXI PUBLICO Y ...</td>
      <td>INVESTIGACIÓN EN IZTAPALAPA</td>
      <td>IZP-6</td>
      <td>...</td>
      <td>IZTAPALAPA</td>
      <td>NaN</td>
      <td>-99.04765</td>
      <td>19.38716</td>
      <td>NaN</td>
      <td>POINT (-99.04765 19.38716)</td>
      <td>1269</td>
      <td>EJTO CONSTITUCIONALISTA, SUPERMANZANA I ( U HAB)</td>
      <td>09007</td>
      <td>0119</td>
    </tr>
    <tr>
      <th>3</th>
      <td>751819</td>
      <td>2019</td>
      <td>Septiembre</td>
      <td>2019-09-14 12:00:00</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07T21:57:48</td>
      <td>FRAUDE</td>
      <td>INVESTIGACIÓN EN BENITO JUÁREZ</td>
      <td>BJ-3</td>
      <td>...</td>
      <td>BENITO JUAREZ</td>
      <td>NaN</td>
      <td>-99.16102</td>
      <td>19.38601</td>
      <td>NaN</td>
      <td>POINT (-99.16102 19.38601)</td>
      <td>936</td>
      <td>NARVARTE V</td>
      <td>09014</td>
      <td>0111</td>
    </tr>
    <tr>
      <th>4</th>
      <td>751820</td>
      <td>2019</td>
      <td>Agosto</td>
      <td>2019-08-13 13:00:00</td>
      <td>2019</td>
      <td>Octubre</td>
      <td>2019-10-07T21:59:40</td>
      <td>VIOLENCIA FAMILIAR</td>
      <td>JUZGADOS FAMILIARES</td>
      <td>CJM-TLP</td>
      <td>...</td>
      <td>ALVARO OBREGON</td>
      <td>NaN</td>
      <td>-99.23382</td>
      <td>19.37586</td>
      <td>NaN</td>
      <td>POINT (-99.23382 19.37586)</td>
      <td>1051</td>
      <td>JALALPA TEPITO</td>
      <td>09010</td>
      <td>013</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 25 columns</p>
</div>



```python
victimas = agrega_ids_espaciales(victimas)
victimas.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>_id</th>
      <th>idCarpeta</th>
      <th>Ano_inicio</th>
      <th>Mes_inicio</th>
      <th>FechaInicio</th>
      <th>delito</th>
      <th>categoria</th>
      <th>Sexo</th>
      <th>Edad</th>
      <th>TipoPersona</th>
      <th>...</th>
      <th>ColoniaHechos</th>
      <th>Calle_hechos</th>
      <th>Calle_hechos2</th>
      <th>latitud</th>
      <th>longitud</th>
      <th>geometry</th>
      <th>colonia_cve</th>
      <th>colonia_nombre</th>
      <th>municipio_cvegeo</th>
      <th>cuadrante_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>595358</td>
      <td>8960172</td>
      <td>2021</td>
      <td>Junio</td>
      <td>2021-06-26T00:00:00</td>
      <td>ROBO DE VEHICULO DE SERVICIO PARTICULAR CON VI...</td>
      <td>ROBO DE VEHÍCULO CON Y SIN VIOLENCIA</td>
      <td>Masculino</td>
      <td>25</td>
      <td>FISICA</td>
      <td>...</td>
      <td>PUERTA GRANDE</td>
      <td>AVENIDA CENTENARIO   CASI ESQUINA CON LA CALLE...</td>
      <td>NaN</td>
      <td>19.3571148543388</td>
      <td>-99.2289503701792</td>
      <td>POINT (-99.22895 19.35711)</td>
      <td>1121</td>
      <td>LOMAS DE PUERTA GRANDE</td>
      <td>09010</td>
      <td>017</td>
    </tr>
    <tr>
      <th>1</th>
      <td>595359</td>
      <td>8960173</td>
      <td>2021</td>
      <td>Junio</td>
      <td>2021-06-26T00:00:00</td>
      <td>ROBO A TRANSPORTISTA Y VEHICULO PESADO CON VIO...</td>
      <td>ROBO A TRANSPORTISTA CON Y SIN VIOLENCIA</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>MORAL</td>
      <td>...</td>
      <td>INDUSTRIAL VALLEJO</td>
      <td>AVENIDA CEYLAN</td>
      <td>ENTRE CERRADA CEYLAN</td>
      <td>19.4938324187342</td>
      <td>-99.1699397596072</td>
      <td>POINT (-99.16994 19.49383)</td>
      <td>80</td>
      <td>INDUSTRIAL VALLEJO (U HAB)</td>
      <td>09002</td>
      <td>022</td>
    </tr>
    <tr>
      <th>2</th>
      <td>595360</td>
      <td>8960173</td>
      <td>2021</td>
      <td>Junio</td>
      <td>2021-06-26T00:00:00</td>
      <td>ROBO A TRANSPORTISTA Y VEHICULO PESADO CON VIO...</td>
      <td>ROBO A TRANSPORTISTA CON Y SIN VIOLENCIA</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>MORAL</td>
      <td>...</td>
      <td>INDUSTRIAL VALLEJO</td>
      <td>AVENIDA CEYLAN</td>
      <td>ENTRE CERRADA CEYLAN</td>
      <td>19.4938324187342</td>
      <td>-99.1699397596072</td>
      <td>POINT (-99.16994 19.49383)</td>
      <td>80</td>
      <td>INDUSTRIAL VALLEJO (U HAB)</td>
      <td>09002</td>
      <td>022</td>
    </tr>
    <tr>
      <th>3</th>
      <td>595361</td>
      <td>8960175</td>
      <td>2021</td>
      <td>Junio</td>
      <td>2021-06-26T00:00:00</td>
      <td>ROBO A NEGOCIO SIN VIOLENCIA POR FARDEROS (TIE...</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>MORAL</td>
      <td>...</td>
      <td>GUADALUPE DEL MORAL</td>
      <td>AVENIDA JAVIER ROJO GOMEZ</td>
      <td>NaN</td>
      <td>19.3681183577951</td>
      <td>-99.0814492098267</td>
      <td>POINT (-99.08145 19.36812)</td>
      <td>1351</td>
      <td>GUADALUPE DEL MORAL</td>
      <td>09007</td>
      <td>0120</td>
    </tr>
    <tr>
      <th>4</th>
      <td>595362</td>
      <td>8960176</td>
      <td>2021</td>
      <td>Junio</td>
      <td>2021-06-26T00:00:00</td>
      <td>FRAUDE</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>Masculino</td>
      <td>37</td>
      <td>FISICA</td>
      <td>...</td>
      <td>NAPOLES</td>
      <td>ARIZONA</td>
      <td>PENSILVANIA</td>
      <td>19.3927810885787</td>
      <td>-99.1806440001974</td>
      <td>POINT (-99.18064 19.39278)</td>
      <td>242</td>
      <td>NAPOLES</td>
      <td>09014</td>
      <td>011</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 28 columns</p>
</div>



### Agregar categorías de usuario

Para clasificar las carpetas de investigación de acuerdo a una categorización definida por el usuario necesitamos un archivo que relacione la columna delitos de la base de carpetas con las categorías definidas por el usuario

```python
categorias = pd.read_csv("datos/categorias_carpetas.csv")
categorias
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>incidente</th>
      <th>categoria</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>HOMICIDIO POR AHORCAMIENTO</td>
      <td>Homicidios dolosos</td>
    </tr>
    <tr>
      <th>1</th>
      <td>HOMICIDIO POR ARMA BLANCA</td>
      <td>Homicidios dolosos</td>
    </tr>
    <tr>
      <th>2</th>
      <td>HOMICIDIO POR ARMA DE FUEGO</td>
      <td>Homicidios dolosos</td>
    </tr>
    <tr>
      <th>3</th>
      <td>HOMICIDIO POR GOLPES</td>
      <td>Homicidios dolosos</td>
    </tr>
    <tr>
      <th>4</th>
      <td>HOMICIDIOS INTENCIONALES (OTROS)</td>
      <td>Homicidios dolosos</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>73</th>
      <td>ROBO DE VEHICULO DE SERVICIO PÚBLICO CON VIOLE...</td>
      <td>Robo de/en vehículo</td>
    </tr>
    <tr>
      <th>74</th>
      <td>ROBO DE VEHICULO DE SERVICIO PÚBLICO SIN VIOLE...</td>
      <td>Robo de/en vehículo</td>
    </tr>
    <tr>
      <th>75</th>
      <td>ROBO DE VEHICULO ELECTRICO MOTOPATIN</td>
      <td>Robo de/en vehículo</td>
    </tr>
    <tr>
      <th>76</th>
      <td>OBO DE VEHICULO EN PENSION, TALLER Y AGENCIAS C/V</td>
      <td>Robo de/en vehículo</td>
    </tr>
    <tr>
      <th>77</th>
      <td>ROBO DE VEHICULO EN PENSION, TALLER Y AGENCIAS...</td>
      <td>Robo de/en vehículo</td>
    </tr>
  </tbody>
</table>
<p>78 rows × 2 columns</p>
</div>



Entonces podemos agregar las categorías a nuestra base

```python
carpetas = agregar_categorias_carpetas(carpetas)
carpetas[['delito', 'categoria']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>delito</th>
      <th>categoria</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>DAÑO EN PROPIEDAD AJENA INTENCIONAL</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ROBO DE VEHICULO DE SERVICIO PARTICULAR CON VI...</td>
      <td>Robo de/en vehículo</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NARCOMENUDEO POSESION SIMPLE</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ROBO A TRANSEUNTE EN VIA PUBLICA CON VIOLENCIA</td>
      <td>Robo a transeúnte</td>
    </tr>
    <tr>
      <th>4</th>
      <td>DENUNCIA DE HECHOS</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1217266</th>
      <td>ABUSO DE AUTORIDAD Y USO ILEGAL DE LA FUERZA P...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1217267</th>
      <td>ROBO A NEGOCIO CON VIOLENCIA</td>
      <td>Robo a negocio</td>
    </tr>
    <tr>
      <th>1217268</th>
      <td>DAÑO EN PROPIEDAD AJENA INTENCIONAL A BIENES I...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1217269</th>
      <td>ALLANAMIENTO DE MORADA, DESPACHO, OFICINA O ES...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1217270</th>
      <td>ROBO A TRANSEUNTE EN VIA PUBLICA CON VIOLENCIA</td>
      <td>Robo a transeúnte</td>
    </tr>
  </tbody>
</table>
<p>1217271 rows × 2 columns</p>
</div>



Algo similar se puede hacer para los datos de Víctimas, en este caso el archivo de categorías es un poco diferente

```python
categorias_victimas = pd.read_csv("datos/categorias_victimas.csv")
categorias_victimas
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Delito</th>
      <th>Categoria</th>
      <th>Cantidad</th>
      <th>Nivel 1</th>
      <th>Nivel 2</th>
      <th>Nivel 3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ABORTO</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>168</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ABUSO DE AUTORIDAD Y USO ILEGAL DE LA FUERZA P...</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>5924</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ABUSO DE CONFIANZA</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>12050</td>
      <td>Abuso de Confianza</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ABUSO SEXUAL</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>10238</td>
      <td>Abuso Sexual</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ACOSO SEXUAL</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>2986</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>295</th>
      <td>VIOLACION TUMULTUARIA</td>
      <td>VIOLACIÓN</td>
      <td>74</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>296</th>
      <td>VIOLACION TUMULTUARIA EQUIPARADA</td>
      <td>VIOLACIÓN</td>
      <td>4</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>297</th>
      <td>VIOLACION TUMULTUARIA EQUIPARADA POR CONOCIDO</td>
      <td>VIOLACIÓN</td>
      <td>2</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>298</th>
      <td>VIOLACION Y ROBO DE VEHICULO</td>
      <td>VIOLACIÓN</td>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>299</th>
      <td>VIOLENCIA FAMILIAR</td>
      <td>DELITO DE BAJO IMPACTO</td>
      <td>94592</td>
      <td>Violencia Familiar</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>300 rows × 6 columns</p>
</div>



Las columnas importantes son `Nivel 1` y `Nivel 2` (podría haber más niveles), esas definen las categorías que se van a asignar a cada fila que se una a los datos de víctimas via la columna `Delito`

```python
victimas = agregar_categorias_victimas(victimas)
victimas[['Delito', 'Nivel 1', 'Nivel 2', 'Nivel 3']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Delito</th>
      <th>Nivel 1</th>
      <th>Nivel 2</th>
      <th>Nivel 3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ROBO DE VEHICULO DE SERVICIO PARTICULAR CON VI...</td>
      <td>Robo de Vehículo de Servicio Particular</td>
      <td>Con Violencia</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ROBO A TRANSPORTISTA Y VEHICULO PESADO CON VIO...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ROBO A TRANSPORTISTA Y VEHICULO PESADO CON VIO...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ROBO A NEGOCIO SIN VIOLENCIA POR FARDEROS (TIE...</td>
      <td>Robo a Negocio y Tiendas de Autoservicio</td>
      <td>Sin Violencia</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>FRAUDE</td>
      <td>Fraude</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>90</th>
      <td>NARCOMENUDEO POSESION SIMPLE</td>
      <td>Narcomenudeo</td>
      <td>Posesión Simple</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>91</th>
      <td>DAÑO EN PROPIEDAD AJENA CULPOSA POR TRÁNSITO V...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>92</th>
      <td>ROBO A TRANSEUNTE EN NEGOCIO CON VIOLENCIA</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>93</th>
      <td>LESIONES CULPOSAS POR TRANSITO VEHICULAR EN CO...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>94</th>
      <td>DAÑO EN PROPIEDAD AJENA CULPOSA POR TRÁNSITO V...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>95 rows × 4 columns</p>
</div>



### Exportar datos para el visualizador

```python
exporta_datos_visualizador(carpetas, "datos/salidas/carpetas.csv", tipo='carpetas')
exporta_datos_visualizador(victimas, "datos/salidas/victimas.csv", tipo='victimas')
```

### Serie de tiempo por categoría

````Python
serie = serie_de_tiempo_categoria(carpetas_todas, pd.to_datetime('01/01/2016'), 'Robo a pasajero')
````

### Serie de tiempo por geografía y categoría
````Python
serie = serie_tiempo_categorias_unidades(victimas, pd.to_datetime('01/01/2019'))
````

## Patrones espacio temporales

Este módulo tiene diferentes herramientas para explorar los patrones espacio-temporales de la actividad delictiva
````Python
from criminologia_cdmx.patrones_espacio_temporales import *
````

### Estimación de densidad de kernel
A partir de cualquier capa de incidentes se puede estimar el KDE utilizando validación cruzada para encontrar el mejor bandwidth

```python
carpetas = get_carpetas_from_api(1000)
x = carpetas.geometry.x.to_numpy()
y = carpetas.geometry.y.to_numpy()
params = {'bandwidth': np.linspace(0.001, 0.1, 100)}
bw = ajusta_bandwidth_kde(x, y, params)
xx, yy, zz = kde2D(x, y, bw, xbins=100j, ybins=100j)
fig = plt.figure(figsize=(10,10))
ax = plt.axes(projection='3d')
ax.plot_surface(xx, yy, zz,cmap='viridis', edgecolor='none')
```




    <mpl_toolkits.mplot3d.art3d.Poly3DCollection at 0x7f2122d15d00>




![png](docs/images/output_28_1.png)


### Serie de tiempo de KDEs por categoría

Para una categoría determinada se obtiene la serie de tiempo de densidades de Kernel para un periodo arbitrario, utilizando la agregación temporal determinada por el usuario.

Para usar esta función no es necesario agregar los ids de unidades espaciales.

````Python

carpetas = get_carpetas_desde_archivo()
carpetas = agregar_categorias_carpetas(carpetas)
fechas = pd.date_range(start='1/1/2019', end='1/1/2021', freq='M').to_list()
xx, yy, kdes = serie_tiempo_kde_categoria(carpetas, 
                                          fechas, 
                                          ["Homicidios dolosos"], 
                                          "30 days")
````

Ya teniendo la serie de KDEs es relatívamente fácil obtener una animación de la evolución utilizando el siguiente código. Es necesario instalar la extensión [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/):
````Python

import matplotlib.animation as animation
def data(t):
    d = kdes[t]
    ax.clear()
    surf = ax.plot_surface(XX, YY, d[2], cmap='viridis', edgecolor='none', 
                           antialiased=False)
    ax.set_zlim([0,50]) 


fig = plt.figure(figsize=(10,10))
ax = fig.gca(projection='3d')
surf = ax.plot_surface(xx, yy, kdes[0][2],cmap='viridis', edgecolor='none', antialiased=False)
ax.set_zlim(0, 50)
ani = animation.FuncAnimation(fig, data, len(kdes), interval=50, repeat=False )
plt.show()
````

### Mapas de intensidad relativa y significancia

Además de producir las superficies de probabilidad para cada categoría de delitos, es posible comparar dos categorías y estimar la significancia de las diferencias

```python
carpetas_todas = get_carpetas_desde_archivo('datos/descargas/carpetas_fiscalia.csv')
carpetas_todas = agregar_categorias_carpetas(carpetas_todas)
fechas = pd.date_range(start='1/1/2019', end='3/1/2019', freq='M').to_list()
razones, intensidades = serie_mapas_intensidad(carpetas_todas, 
                                               fechas,
                                               'Homicidios dolosos',
                                               "30 days", bw=0.001)
significancias = p_value_maps(razones)
fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(15,10))
ax1.imshow(razones[0])
ax1.set_title("Razón de la categoría")
ax2.imshow(intensidades[0])
ax2.set_title("Intensidad de la categoría")
ax3.imshow(significancias[0])
ax3.set_title("Significancia de la intensidad")
```




    Text(0.5, 1.0, 'Significancia de la intensidad')




![png](docs/images/output_31_1.png)


### Agregar en hexágonos

Se puede agregar los datos de carpetas/victimas en hexágonos de Uber H3 usando la función `agrega_en_hexagonos` y pasándole los datos y el nivel de escala. Por ejemplo, para agregar los datos en el nivel 8

```python
carpetas_hex = agrega_en_hexagonos(carpetas, 8)
victimas_hex = agrega_en_hexagonos(victimas, 8)
fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(18, 18))
ax0 = (carpetas_hex
       .to_crs(epsg=3857)
       .plot('incidentes', 
             ax=ax0, 
             legend=True,
             cmap='inferno',
             legend_kwds={'shrink': 0.3},))
ax0.set_title("Carpetas de Investigación")
ax0.set_axis_off()
ctx.add_basemap(ax0, source=ctx.providers.CartoDB.DarkMatterNoLabels)
ax1 = (victimas_hex
       .to_crs(epsg=3857)
       .plot('incidentes', 
             ax=ax1, 
             legend=True,
             cmap='inferno',
             legend_kwds={'shrink': 0.3}))
ax1.set_title("Víctimas en Carpetas de Investigación en 2020")
ax1.set_axis_off()
ctx.add_basemap(ax1, source=ctx.providers.CartoDB.DarkMatterNoLabels)
plt.tight_layout()
```


![png](docs/images/output_33_0.png)


## Covariables

Este módulo contiene diferentes funciones y clases para construir covariables para el analisis de delitos.
````Python
from criminologia_cdmx. covariables import *
````
Antes de utilizar este módulo es necesario descargar los datos:

````Python
descarga_datos_covariables()
````

Después de descargar los datos es posible utilizar todas las funciones del módulo.

### Variables censales

El módulo contiene diferentes funciones para procesar las variables del censo, un flujo típico de trabajo consistiría en:

* Leer el censo a nivel manzana
* Agregar en colonias
* Calcular las tasas de las variables

```python
diccionario = get_diccionario_censo()
censo = get_variables_censo()
agregado = agrega_en_unidades(censo, diccionario, imputacion='random')
agregado = censo_a_tasas(agregado, diccionario)
agregado
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>POBTOT</th>
      <th>POBFEM</th>
      <th>POBMAS</th>
      <th>P_0A2</th>
      <th>P_0A2_F</th>
      <th>P_0A2_M</th>
      <th>P_3YMAS</th>
      <th>P_3YMAS_F</th>
      <th>P_3YMAS_M</th>
      <th>P_5YMAS</th>
      <th>...</th>
      <th>VPH_INTER</th>
      <th>VPH_STVP</th>
      <th>VPH_SPMVPI</th>
      <th>VPH_CVJ</th>
      <th>VPH_SINRTV</th>
      <th>VPH_SINLTC</th>
      <th>VPH_SINCINT</th>
      <th>VPH_SINTIC</th>
      <th>OCUPVIVPAR</th>
      <th>PROM_OCUP_C</th>
    </tr>
    <tr>
      <th>colonia_cve</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>80.0</td>
      <td>0.912500</td>
      <td>0.987500</td>
      <td>1.050000</td>
      <td>1.100000</td>
      <td>0.950000</td>
      <td>1.037500</td>
      <td>1.225000</td>
      <td>1.150000</td>
      <td>0.987500</td>
      <td>...</td>
      <td>1.040541</td>
      <td>0.972973</td>
      <td>1.013514</td>
      <td>1.175676</td>
      <td>1.027027</td>
      <td>1.081081</td>
      <td>1.054054</td>
      <td>0.959459</td>
      <td>86.0</td>
      <td>0.170635</td>
    </tr>
    <tr>
      <th>2</th>
      <td>118.0</td>
      <td>0.966102</td>
      <td>0.932203</td>
      <td>0.872881</td>
      <td>0.915254</td>
      <td>0.838983</td>
      <td>0.940678</td>
      <td>0.949153</td>
      <td>0.864407</td>
      <td>0.822034</td>
      <td>...</td>
      <td>0.895652</td>
      <td>0.947826</td>
      <td>0.895652</td>
      <td>0.843478</td>
      <td>0.869565</td>
      <td>0.982609</td>
      <td>0.852174</td>
      <td>0.913043</td>
      <td>104.0</td>
      <td>0.162500</td>
    </tr>
    <tr>
      <th>3</th>
      <td>25.0</td>
      <td>1.000000</td>
      <td>1.040000</td>
      <td>0.480000</td>
      <td>0.800000</td>
      <td>0.840000</td>
      <td>1.280000</td>
      <td>0.840000</td>
      <td>0.640000</td>
      <td>1.000000</td>
      <td>...</td>
      <td>0.952381</td>
      <td>1.238095</td>
      <td>1.000000</td>
      <td>1.047619</td>
      <td>0.857143</td>
      <td>1.047619</td>
      <td>0.857143</td>
      <td>1.047619</td>
      <td>24.0</td>
      <td>0.198347</td>
    </tr>
    <tr>
      <th>4</th>
      <td>34.0</td>
      <td>1.264706</td>
      <td>1.294118</td>
      <td>1.352941</td>
      <td>1.058824</td>
      <td>1.235294</td>
      <td>1.500000</td>
      <td>1.176471</td>
      <td>1.117647</td>
      <td>1.235294</td>
      <td>...</td>
      <td>0.850000</td>
      <td>0.925000</td>
      <td>0.900000</td>
      <td>0.900000</td>
      <td>1.325000</td>
      <td>1.000000</td>
      <td>1.100000</td>
      <td>0.925000</td>
      <td>54.0</td>
      <td>0.200000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>61.0</td>
      <td>0.934426</td>
      <td>1.262295</td>
      <td>1.213115</td>
      <td>0.983607</td>
      <td>1.065574</td>
      <td>0.983607</td>
      <td>1.147541</td>
      <td>1.163934</td>
      <td>1.180328</td>
      <td>...</td>
      <td>0.971014</td>
      <td>1.072464</td>
      <td>0.840580</td>
      <td>0.884058</td>
      <td>1.028986</td>
      <td>0.956522</td>
      <td>0.797101</td>
      <td>1.043478</td>
      <td>84.0</td>
      <td>0.217054</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1820</th>
      <td>89.0</td>
      <td>1.033708</td>
      <td>0.966292</td>
      <td>0.865169</td>
      <td>1.011236</td>
      <td>1.011236</td>
      <td>1.134831</td>
      <td>0.955056</td>
      <td>1.033708</td>
      <td>1.056180</td>
      <td>...</td>
      <td>1.045977</td>
      <td>1.045977</td>
      <td>0.954023</td>
      <td>0.942529</td>
      <td>1.103448</td>
      <td>1.022989</td>
      <td>0.816092</td>
      <td>1.160920</td>
      <td>94.0</td>
      <td>0.170909</td>
    </tr>
    <tr>
      <th>1821</th>
      <td>209.0</td>
      <td>0.918660</td>
      <td>0.961722</td>
      <td>1.047847</td>
      <td>1.000000</td>
      <td>1.062201</td>
      <td>1.090909</td>
      <td>0.995215</td>
      <td>1.052632</td>
      <td>0.933014</td>
      <td>...</td>
      <td>0.776316</td>
      <td>0.903509</td>
      <td>0.912281</td>
      <td>0.947368</td>
      <td>0.872807</td>
      <td>0.859649</td>
      <td>0.907895</td>
      <td>0.864035</td>
      <td>212.0</td>
      <td>0.175207</td>
    </tr>
    <tr>
      <th>1822</th>
      <td>7.0</td>
      <td>0.857143</td>
      <td>0.285714</td>
      <td>0.714286</td>
      <td>1.142857</td>
      <td>1.285714</td>
      <td>0.857143</td>
      <td>0.857143</td>
      <td>0.428571</td>
      <td>0.571429</td>
      <td>...</td>
      <td>2.200000</td>
      <td>1.400000</td>
      <td>1.800000</td>
      <td>1.400000</td>
      <td>1.000000</td>
      <td>1.200000</td>
      <td>1.200000</td>
      <td>1.200000</td>
      <td>6.0</td>
      <td>0.109091</td>
    </tr>
    <tr>
      <th>1823</th>
      <td>61.0</td>
      <td>0.934426</td>
      <td>1.393443</td>
      <td>1.049180</td>
      <td>1.278689</td>
      <td>1.147541</td>
      <td>1.147541</td>
      <td>1.213115</td>
      <td>1.213115</td>
      <td>1.000000</td>
      <td>...</td>
      <td>0.985075</td>
      <td>1.014925</td>
      <td>1.029851</td>
      <td>1.029851</td>
      <td>1.059701</td>
      <td>0.895522</td>
      <td>0.776119</td>
      <td>1.044776</td>
      <td>88.0</td>
      <td>0.232804</td>
    </tr>
    <tr>
      <th>1824</th>
      <td>13.0</td>
      <td>0.846154</td>
      <td>1.076923</td>
      <td>0.461538</td>
      <td>0.923077</td>
      <td>0.846154</td>
      <td>1.076923</td>
      <td>0.538462</td>
      <td>0.538462</td>
      <td>0.461538</td>
      <td>...</td>
      <td>0.750000</td>
      <td>0.833333</td>
      <td>0.916667</td>
      <td>0.833333</td>
      <td>0.916667</td>
      <td>0.333333</td>
      <td>0.750000</td>
      <td>1.166667</td>
      <td>15.0</td>
      <td>0.250000</td>
    </tr>
  </tbody>
</table>
<p>1809 rows × 212 columns</p>
</div>



### Variables de Uso de Suelo

El módulo de covariables incluye (por lo pronto) algunas pocas variables sobre el uso de suelo:

* Cantidad de usos de comercio al por menor
* Cantidad de usos de industria
* Cantidad de usos de servicios

Estas variables están a nivel manzana, pero por lo pronto no es posible (¿conveniente?) usarlas en esa escala, entonces tenemos un método para agregarlas a nivel cuadrante o colonia (eventualmente habrá forma de usar agregaciones arbitrarias). Cuando se agregan los usos a colonias o cuadrantes se calculan también dos variables extra:

* Intensidad: la cantidad de total de usos de suelo considerados
* Entropía: una medida de la mezcla de los usos de suelo

```python
usos = get_uso_de_suelo()
usos = agrega_uso_suelo(usos, unidades='colonias')
usos
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Industria</th>
      <th>Comercio</th>
      <th>Servicios</th>
      <th>Intensidad</th>
      <th>Entropía</th>
    </tr>
    <tr>
      <th>colonia_cve</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>8</td>
      <td>87</td>
      <td>44</td>
      <td>139</td>
      <td>-4.072303</td>
    </tr>
    <tr>
      <th>2</th>
      <td>15</td>
      <td>112</td>
      <td>55</td>
      <td>182</td>
      <td>-3.803105</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2</td>
      <td>22</td>
      <td>7</td>
      <td>31</td>
      <td>-4.161488</td>
    </tr>
    <tr>
      <th>4</th>
      <td>9</td>
      <td>55</td>
      <td>31</td>
      <td>95</td>
      <td>-3.661970</td>
    </tr>
    <tr>
      <th>5</th>
      <td>31</td>
      <td>144</td>
      <td>66</td>
      <td>241</td>
      <td>-3.514375</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1820</th>
      <td>45</td>
      <td>255</td>
      <td>213</td>
      <td>513</td>
      <td>-3.651524</td>
    </tr>
    <tr>
      <th>1821</th>
      <td>135</td>
      <td>1074</td>
      <td>733</td>
      <td>1942</td>
      <td>-3.852911</td>
    </tr>
    <tr>
      <th>1822</th>
      <td>1</td>
      <td>18</td>
      <td>12</td>
      <td>31</td>
      <td>-4.484460</td>
    </tr>
    <tr>
      <th>1823</th>
      <td>28</td>
      <td>166</td>
      <td>107</td>
      <td>301</td>
      <td>-3.644880</td>
    </tr>
    <tr>
      <th>1824</th>
      <td>6</td>
      <td>24</td>
      <td>25</td>
      <td>55</td>
      <td>-3.489230</td>
    </tr>
  </tbody>
</table>
<p>1809 rows × 5 columns</p>
</div>



### Índices PCA

Para facilitar la construcción de modelos utilizando variables censales, proveemos una clase para construir índices basados en Componentes principales a partir de una lista de variables del Censo.

Construir un índice es muy sencillo, primero se seleccionan un conjunto de variables:

```python
vars_indice = ['P5_HLI', 'POB_AFRO', 'PCON_DISC', 'P3A5_NOA', 
               'P6A11_NOA', 'P12A14NOA', 'P15YM_AN', 'PSINDER', 'PDESOCUP']
diccionario[diccionario['Nombre del Campo'].isin(vars_indice)][['Nombre del Campo', 'Descripción']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Nombre del Campo</th>
      <th>Descripción</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>69</th>
      <td>P5_HLI</td>
      <td>Personas de 5 a 130 años de edad que hablan al...</td>
    </tr>
    <tr>
      <th>73</th>
      <td>POB_AFRO</td>
      <td>Personas que se consideran afromexicanos o afr...</td>
    </tr>
    <tr>
      <th>76</th>
      <td>PCON_DISC</td>
      <td>Personas que realizan con mucha dificultad o n...</td>
    </tr>
    <tr>
      <th>92</th>
      <td>P3A5_NOA</td>
      <td>Personas de 3 a 5 años de edad que no van a la...</td>
    </tr>
    <tr>
      <th>95</th>
      <td>P6A11_NOA</td>
      <td>Personas de 6 a 11 años de edad que no van a l...</td>
    </tr>
    <tr>
      <th>98</th>
      <td>P12A14NOA</td>
      <td>Personas de 12 a 14 años de edad que no van a ...</td>
    </tr>
    <tr>
      <th>110</th>
      <td>P15YM_AN</td>
      <td>Personas de 15 a 130 años de edad que no saben...</td>
    </tr>
    <tr>
      <th>143</th>
      <td>PDESOCUP</td>
      <td>Personas de 12 a 130 años de edad que no tenía...</td>
    </tr>
    <tr>
      <th>146</th>
      <td>PSINDER</td>
      <td>Total de personas que no están afiliadas a ser...</td>
    </tr>
  </tbody>
</table>
</div>



Con la lista de variables se inicializa la clase y se calcula el índice. En este caso vamos a usar los agregados por colonia que calculamos antes.  

```python
indice = IndicePCA(agregado, vars_indice)
indice.calcula_indice()
print(f'El porcentaje de la varianza explicada por el índice es {indice.varianza_explicada[0]}')
```

    El porcentaje de la varianza explicada por el índice es 0.6004451881076397


El DataFrame con los valores del índice se guarda en la propiedad `indice`:

```python
indice.indice
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>colonia_cve</th>
      <th>Índice</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0.184298</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1.687427</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1.540912</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>2.636684</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>1.026860</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1797</th>
      <td>1820</td>
      <td>0.218373</td>
    </tr>
    <tr>
      <th>1798</th>
      <td>1821</td>
      <td>0.318991</td>
    </tr>
    <tr>
      <th>1799</th>
      <td>1822</td>
      <td>0.710312</td>
    </tr>
    <tr>
      <th>1800</th>
      <td>1823</td>
      <td>1.402441</td>
    </tr>
    <tr>
      <th>1801</th>
      <td>1824</td>
      <td>2.263297</td>
    </tr>
  </tbody>
</table>
<p>1802 rows × 2 columns</p>
</div>



## Modelos

Este módulo contiene funciones y clases para ajustar diferentes tipos de modelos para el analisis criminológico.

````Python
from criminologia_cdmx.modelos import *
````

El módulo incluye funciones para procesar variables dependientes, crear capas de análisis y ajustar modelos.

La `CapaDeAnalisis` es la unidad base de este módulo, es un contenedor para las variables dependiente e independientes.

A continuación se muestra un flujo completo para ajustar un modelo GLM usando la familia Binomial Negativa.

### Variable dependiente

```python
carpetas = get_carpetas_from_api(100000)
carpetas = agrega_ids_espaciales(carpetas)
fecha_inicio = carpetas.fecha_hechos.min().strftime("%d-%m.%Y")
fecha_fin = carpetas.fecha_hechos.max().strftime("%d-%m.%Y")
delito = 'ROBO A CASA HABITACION SIN VIOLENCIA'
Y = variable_independiente(carpetas, 'delito', delito, fecha_inicio, fecha_fin)
```

### Covariables
Para este ejemplo sólo vamos a usar uso de suelo

```python
usos = get_uso_de_suelo()
usos = agrega_uso_suelo(usos, unidades='colonias')
```

### Capa de Análisis

```python
ca = CapaDeAnalisis(Y, usos, 'colonia_cve')
```

### Creación y ajuste de modelo

```python
m = ModeloGLM(ca, sm.families.NegativeBinomial())
fm = m.fit()
fm.summary()
```




<table class="simpletable">
<caption>Generalized Linear Model Regression Results</caption>
<tr>
  <th>Dep. Variable:</th>   <td>Q('ROBO A CASA HABITACION SIN VIOLENCIA')</td> <th>  No. Observations:  </th>  <td>  1623</td> 
</tr>
<tr>
  <th>Model:</th>                              <td>GLM</td>                    <th>  Df Residuals:      </th>  <td>  1618</td> 
</tr>
<tr>
  <th>Model Family:</th>                <td>NegativeBinomial</td>              <th>  Df Model:          </th>  <td>     4</td> 
</tr>
<tr>
  <th>Link Function:</th>                      <td>log</td>                    <th>  Scale:             </th> <td>  1.0000</td>
</tr>
<tr>
  <th>Method:</th>                            <td>IRLS</td>                    <th>  Log-Likelihood:    </th> <td> -1441.2</td>
</tr>
<tr>
  <th>Date:</th>                        <td>Tue, 29 Mar 2022</td>              <th>  Deviance:          </th> <td>  1145.1</td>
</tr>
<tr>
  <th>Time:</th>                            <td>19:51:09</td>                  <th>  Pearson chi2:      </th> <td>1.24e+03</td>
</tr>
<tr>
  <th>No. Iterations:</th>                     <td>100</td>                    <th>                     </th>     <td> </td>   
</tr>
<tr>
  <th>Covariance Type:</th>                 <td>nonrobust</td>                 <th>                     </th>     <td> </td>   
</tr>
</table>
<table class="simpletable">
<tr>
         <td></td>            <th>coef</th>     <th>std err</th>      <th>z</th>      <th>P>|z|</th>  <th>[0.025</th>    <th>0.975]</th>  
</tr>
<tr>
  <th>Intercept</th>       <td>   -1.8829</td> <td>    0.314</td> <td>   -5.989</td> <td> 0.000</td> <td>   -2.499</td> <td>   -1.267</td>
</tr>
<tr>
  <th>Q('Industria')</th>  <td>    0.0031</td> <td>    0.001</td> <td>    2.694</td> <td> 0.007</td> <td>    0.001</td> <td>    0.005</td>
</tr>
<tr>
  <th>Q('Comercio')</th>   <td>   -0.0024</td> <td>    0.000</td> <td>   -5.557</td> <td> 0.000</td> <td>   -0.003</td> <td>   -0.002</td>
</tr>
<tr>
  <th>Q('Servicios')</th>  <td>    0.0013</td> <td>    0.000</td> <td>    2.736</td> <td> 0.006</td> <td>    0.000</td> <td>    0.002</td>
</tr>
<tr>
  <th>Q('Intensidad')</th> <td>    0.0019</td> <td>    0.000</td> <td>    6.050</td> <td> 0.000</td> <td>    0.001</td> <td>    0.003</td>
</tr>
<tr>
  <th>Q('Entropía')</th>   <td>   -0.1445</td> <td>    0.081</td> <td>   -1.790</td> <td> 0.074</td> <td>   -0.303</td> <td>    0.014</td>
</tr>
</table>


