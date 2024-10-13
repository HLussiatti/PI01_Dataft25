# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>
# <h2 align=center>**Sistema de recomendación de Juegos de Steam**</h2>


# **CONSINGNA:**
Steam pide que te encargues de crear un sistema de recomendación de videojuegos para usuarios.

Tener un MVP (Minimum Viable Product) para el cierre del proyecto! 


# TAREAS REALIZADAS:
**1. Ingesta de datos**

    - La carga de datos se desarrolló en el notebook: "1. ExtractData."
    - La ingesta se realizó de forma directa, desanidando los datos necesarios y tratando de optimizar la carga directa manejando los archivos como diccionarios y luego cargandolos en un DataFrame. 
    - Los datos se guardaron en archivos del tipo parquet para lograr mayor compresión y poder consumirlos luego con mayor velocidad.
    - No se realizaron modificaciones a los datos en esta instancia salvo en el caso del campo "price" del archivo "steam_games" el cual requirió ser transformado a texto para poder ser guardado como parquet.

    - En esta instancia se obtuvieron los archivos guardados en datasets/1. Extracción: steam_games.parquet, user_reviews.parquet y users_items.parquet  

**2. Tratamiento de datos (duplicados, outliers, nulos)**

    - Se realizó un análisis básico de duplicados, faltantes y outliers en el notebook "2. TransformData"
    - Se normalizan campos llevandolos a los tipos de datos que correspondan.
    - En esta instancia se obtuvieron los archivos guardados en datasets/2. Depurado: steam_games_depurado.parquet, user_reviews_depurado.parquet y users_items_depurado.parquet
    

    VER SI PUEDO AGREGAR COLUMNAS CON LAS MODIFICACIONES REALIZDAS SOBRE EL DF

**3. Se elabora el NLP**

    - Es necesario elaborar el análisis de Lenguaje Natural para poder usar el resultado en la API. Se desarrolló en la notebook "3. NLP"
    - Para ello se realizó la tokenización, la eliminación de expresiones regulares y la lematización para luego procesar estos resultados utiilizando la biblioteca textblob.
    - Se realizó una prueba con la biblioteca "Transformers" pero se demora mucho en correr sin una buena GPU. Si hubiera tiempo se realizará este análisis.
    - Se obtuvo el archivo guardado en datasets/2. Depurado: user_reviews_NLP.parquet

**4. Creación de las funciones.**

    - Se crearon las funciones en el notebook "4. FastAPI". Estas funciones serán las cargadas en la API.
    - Se optimizaron para poder ser procesadas posteriormente en Render.

**5. FastAPI**
    
    - Es necesario instalar fastapi y uvicorn
    - Se creó una estructura de proyecto en PI01_FastAPI
    - Se probó todo de forma local realizando las modificaciones necesarias a los archivos, como por ejemplo:
        - El resultado de las funciones tiene que ser un json para que funcione el framework de FastAPI por lo que se hicieron algunas modificaciones en fuctions.py


        RECORDAR TRANSFORAR MINUTOS A HORAS
    

**6. Deploymet en Render**

    - En primer lguar se elaboró el archivo de requirements.txt con las librerías mínimas necesarias para el funcionamiento de la API.
        - Si bien este archivo inicialmente se elaboró a partir del la creación de un entorno virtual, es mejor hacerlo manualmente utilizando sólo las librerías mínimas necesarias.   
    - Luego se creó una cuenta en Redener y se creó el siguiente entorno: https://pi01-dataft25.onrender.com/
    - Se debieron adaptar las funciones creadas en el notbook "4. FastAPI" para funcionar en Render.
        - Por ejemplo, render utiliza "/" en lugar de "\\"
        - Como la API parsea las URLs, se deben modificar algunas cosas:
            - Se utiliza año como "anio"
            - Se utilza la librería unquote para decodificar casos como por ejemplo, nombres de desarrolladores con espacios.

**7. EDA**
    - Se realizó el análisis de las variables más relevantes para el desarrollo del modelo ML.
        - Se eliminaron algunos valores de género que no era descriptivos (Free To Play, Early Access)
    - En esta intancia se agregaron algunas métricas al archivo steam_games con el objetivo de buscar patrones:
        - Se agregaron métricas de recomendaciones
        - Se agregaron métricas de valorización de reviews del NLP
    - No se detectaron relaciones o correlaciones siginificativas entre los datos de ningún tipo.
    - Esto puede deberse a la mala calidad de los datos.
    - Por este motivo el modelo de basará fundamentalmente en las caracterísiticas de los juegos: géneros, especificaciones y tags.
    - 

**8. ML**
    - Tomando los datos

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

Userdata: devuelve la cantidad de dinero gastado por usuario, el porcentaje de recomendación en base a reviews.recommend y cantida de items.