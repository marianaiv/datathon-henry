<h1 align="center"> Datathon :rocket: </h1>

> Repositorio para el datathon del bootcamp Soy Henry.  

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# **Tabla de Contenidos:**

- [**Tabla de Contenidos:**](#tabla-de-contenidos)
- [El datathon <a name="datathon"></a>](#el-datathon-)
- [Sobre el repositorio <a name="about_repo"></a>](#sobre-el-repositorio-)
- [Notebook <a name="notebook"></a>](#notebook-)


# El datathon <a name="datathon"></a>
El datathon es parte de la etapa de proyectos individuales del bootcamp Soy Henry. En este caso, se trató un problema de clasificación relacionado al mercado inmobiliario. El objetivo fue desarrollar un modelo de aprendizaje automático capaz de clasificar si una propiedad era barata o cara, tomando como frontera de división entre estas dos categorías la media de precios.

Para el datathon nos proporcionaron los datos que se encuentran disponibles en el archivo zip en la carpeta datasets: un conjunto de training, con los precios de las propiedades y un conjunto de testing sin los precios de las propiedades, para realizar las predicciones.

# Sobre el repositorio <a name="about_repo"></a>
En el repositorio se encuentra el notebook `modelos.ipynb`, donde se realizó el EDA, se entrenaron modelos para medir su rendimiento y se obtuvieron las predicciones.

En la carpeta *datasets* se encuentra el zip con los datos. Este debe ser descomprimido en la misma carpeta para que el notebook corra.

# Notebook <a name="notebook"></a>
El notebook esta organizado de la siguiente manera:
- **El EDA**: En esta parte encontramos la limpieza, calculos y visualización de variables. Las transformaciones principales que contribuyeron a los datos utilizados en la parte de entrenamiento se encuentran en funciones.
- **Prueba de modelos**: por ahora se probaron 3 modelos distintos con distintas combinaciones de los datos obtenidos del EDA.
- **Predicción**: Se escogió el modelo con mejor resultado para hacer las predicciones. En esta parte se hicieron las transformaciones pertinentes al set de prueba y se guardan las predicciones como un csv.
