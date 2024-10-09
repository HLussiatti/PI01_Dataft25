<<<<<<< HEAD
# CONSINGNA:
Steam pide que te encargues de crear un sistema de recomendación de videojuegos para usuarios.

Tener un MVP (Minimum Viable Product) para el cierre del proyecto! 


# PASOS A SEGUIR:
1. Ingesta de datos

    - La carga de datos se desarrolló en el notebook: "1. ExtractData."
    - La ingesta se realizó de forma directa, desanidando los datos necesarios y tratando de optimizar la carga directa manejando los archivos como diccionarios y luego cargandolos en un DataFrame. 
    - Los datos se guardaron en archivos del tipo parquet para lograr mayor compresión y poder consumirlos luego con mayor velocidad.
    - No se realizaron modificaciones a los datos en esta instancia salvo en el caso del campo "price" del archivo "steam_games" el cual requirió ser transformado a texto para poder ser guardado como parquet.

    - En esta instancia obtuve: steam_games.parquet, user_reviews.parquet y users_items.parquet  

2. Tratamiento de datos (duplicados, outliers, nulos)

    - Se realizó un análisis básico de duplicados, faltantes y outliers en el notebook "2. TransformData"
    - En esta instancia obtuve: steam_games_depurado.parquet y users_items_depurado.parquet  
    - Además se generaron los archivos steam_games_dep_reduced.parquet y users_items_dep_reduced.parquet con los datos extrictamente necesarios para ser consumidos por la Api.

3. Elaboramos el NLP

    - Es necesario elaborar el análisis de Lenguaje Natural para poder usar el resultado en la API. Se desarrolló en la notebook "3. NLP"
    - Para ello se realizó la tokenización, la eliminación de expresiones regulares y la lematización para luego ingresar con estos resultados a la biblioteca textblob.
    - Se realizó una prueba con la biblioteca "Transformers" pero se demora mucho en correr sin una buena GPU. Si hay tiempo se realizará este análisis.

4. Creación de las funciones.

    - Creamos las funciones en el notebook "4. FastAPI".

5. FastAPI
    
    - Es necesario instalar fastapi y uvicorn
    - Creo una estructura de proyecto en PI01_FastAPI
    - El resultado de las funciones tiene que ser un json para que funcione el framework de FastAPI.
    - Año no funciona, se pasa como anio.



4. Deploymet
5. ML
6. EDA y Entrenamiento
7. Modelo
8. Infraestructura para la puesta en marcha y nuevos datos
9. Modelo usandose en una app


# TRANSFORMACIONES:
No se solicitn transformaciones específicas.
Se debe trabajar en leer el dataseet con el formato correcto.
Eliminar columnas que no sean necesarias para responder las consultas o prerparar los modelos.

# FEATURE ENGINEERING:
Crear "Sentiment_Analysis" aplicando NLP a las revires de "User_Reviews".

# DESARROLLO API: 
Disponibilizar los datos en el Framework FastAPI. https://fastapi.tiangolo.com/tutorial/

Se deben crear 5 funciones (endpoints).

Developer: cantidad de ítems y porcentaje de contenido Free por año según empresa desarrolladora.

=======
# CONSINGNA:
Steam pide que te encargues de crear un sistema de recomendación de videojuegos para usuarios.

Tener un MVP (Minimum Viable Product) para el cierre del proyecto! 


# PASOS A SEGUIR:
1. Ingesta de datos

    - La carga de datos se desarrolló en el notebook: "1. ExtractData."
    - La ingesta se realizó de forma directa, desanidando los datos necesarios y tratando de optimizar la carga directa manejando los archivos como diccionarios y luego cargandolos en un DataFrame. 
    - Los datos se guardaron en archivos del tipo parquet para lograr mayor compresión y poder consumirlos luego con mayor velocidad.
    - No se realizaron modificaciones a los datos en esta instancia salvo en el caso del campo "price" del archivo "steam_games" el cual requirió ser transformado a texto para poder ser guardado como parquet.

    - En esta instancia obtuve: steam_games.parquet, user_reviews.parquet y users_items.parquet  

2. Tratamiento de datos (duplicados, outliers, nulos)

    - Se realizó un análisis básico de duplicados, faltantes y outliers en el notebook "2. TransformData"
    - En esta instancia obtuve: steam_games_depurado.parquet y users_items_depurado.parquet  
    - Además se generaron los archivos steam_games_dep_reduced.parquet y users_items_dep_reduced.parquet con los datos extrictamente necesarios para ser consumidos por la Api.

3. Elaboramos el NLP

    - Es necesario elaborar el análisis de Lenguaje Natural para poder usar el resultado en la API. Se desarrolló en la notebook "3. NLP"
    - Para ello se realizó la tokenización, la eliminación de expresiones regulares y la lematización para luego ingresar con estos resultados a la biblioteca textblob.
    - Se realizó una prueba con la biblioteca "Transformers" pero se demora mucho en correr sin una buena GPU. Si hay tiempo se realizará este análisis.

4. Creación de las funciones.

    - Creamos las funciones en el notebook "4. FastAPI".

5. FastAPI
    
    - Es necesario instalar fastapi y uvicorn
    - Creo una estructura de proyecto en PI01_FastAPI
    - El resultado de las funciones tiene que ser un json para que funcione el framework de FastAPI.
    - Año no funciona, se pasa como anio.



4. Deploymet
5. ML
6. EDA y Entrenamiento
7. Modelo
8. Infraestructura para la puesta en marcha y nuevos datos
9. Modelo usandose en una app


# TRANSFORMACIONES:
No se solicitn transformaciones específicas.
Se debe trabajar en leer el dataseet con el formato correcto.
Eliminar columnas que no sean necesarias para responder las consultas o prerparar los modelos.

# FEATURE ENGINEERING:
Crear "Sentiment_Analysis" aplicando NLP a las revires de "User_Reviews".

# DESARROLLO API: 
Disponibilizar los datos en el Framework FastAPI. https://fastapi.tiangolo.com/tutorial/

Se deben crear 5 funciones (endpoints).

Developer: cantidad de ítems y porcentaje de contenido Free por año según empresa desarrolladora.

>>>>>>> 1e33531cfa27d57b672fef2a4ae0b82ffb19a835
Userdata: devuelve la cantidad de dinero gastado por usuario, el porcentaje de recomendación en base a reviews.recommend y cantida de items.