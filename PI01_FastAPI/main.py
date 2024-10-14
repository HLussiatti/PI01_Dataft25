# app.py

import pandas as pd
import numpy as np
from fastapi import FastAPI
from urllib.parse import unquote
from functions import developer
from functions import userdata
from functions import UserForGenre
from functions import best_developer_year
from functions import developer_reviews_analysis
from modelo_ML import recommend_games



app = FastAPI()


@app.get("/developer/{desarrolladora}")
def read_developer_reviews(desarrolladora: str):
    """
    Endpoint para obtener la cantidad de items y porcentaje 
    de contenido Free por año de lanzamiento del juego 
    para la empresa desarrolladora ingresada.
    
    Parámetros:
    -----------
    desarrolladora: str
        Es la desarrolladora del Juego.

    Devuelve:
    -----------
    "year": 
        Años en los que hay juegos lanzados para la desarrolladora.
    "total_items": 
        Cantidad de Juegos lanzados en el año por la desarrolladora.
    "free_items": 
        Cantidad de Juegos Free lanzados en el año por la desarrolladora.
    "percentage_free": 
        Porcentaje de Juegos Free respecto del total.     
    """
    
    # Cuando paso una desarrolladora que tiene algún espacio en el medio, lo parsea.
    # Ejemplo: “Bohemia Interactive” pasa a ser "Bohemia%20Interactive".
    # Tengo que decodificar los caracteres de la URL con unquote.
    # Aplica a todas las funciones por las dudas.

    resultado = developer(unquote(desarrolladora))
    return  resultado


@app.get("/userdata/{user_id}")
def read_userdata(user_id: str):
    """
    Endpoint para obtener la cantidad de dinero gastado por el usuario, 
    el porcentaje de recomendación en base a reviews.recommend y 
    la cantidad de items que posee el usuario.
    
    Parámetros:
    -----------
    user_id: str
        Es el identificador único del usuario. 

    Devuelve:
    -----------
    "Usuario": 
        Id del Usuario ingresado.
    "Dinero gastado": 
        Total de dinero gastado por el Usuario
    "% de recomendación":
        Porcentaje de Juegos recomendados sobre el total de recomendaciones realizadas.
    "Cantidad de items":
        Cantidad de Juegos que posee el Usuario.
    """
    result = userdata(unquote(user_id))
    return result

@app.get("/UserForGenre/{genero}")
def read_UserForGenre(genero: str):
    """
    Endpoint para obtener el Usuario que acumula más horas jugadas para 
    el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.
    
    Parámetros:
    -----------
    genero: str
        Un género de Juegos. 

    Devuelve:
    -----------
    "Usuario con más horas jugadas para Género Racing": 
        Usuario con más cantidad de horas jugadas en la historia para el género solicitado género.
    "Horas jugadas": [
        "Año": 
            Año de lanzamiento.
        "Horas":
            Cantidad de horas jugadas por el Usuario con más horas jugadas para el género.
    """    
    result = UserForGenre(unquote(genero))
    return result

@app.get("/best_developer_year/{anio}" )
def read_best_developer_year(anio: int):
    """
    Endpoint para obtener el top 3 de desarrolladores con juegos más recomendados 
    por usuarios para el año dado. (reviews.recommend = True y comentarios positivos).

    Parámetros:
    -----------
    anio: int
        Año para el cual se requiere el top 3 de desarrolladores.
    
    Devuelve:
    -----------
    "Puesto 1": Primer puesto
    "Puesto 2": Segundo puesto
    "Puesto 3": Tercer puesto
    """
    result = best_developer_year(anio)
    return result

@app.get("/developer_reviews_analysis/{desarrolladora}")
def read_developer_reviews_analysis(desarrolladora: str):
    """
    Endpoint para obtener un diccionario con el nombre del desarrollador 
    como llave y una lista con la cantidad total de registros de reseñas de 
    suarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.

    Parámetros:
    -----------
    desarrolladora: str
        Es la desarrolladora del Juego.

    Devuelve:
    -----------
    desarrolladora:
        Es la desarrolladora ingresada. 
    Negativos:
        Es la cantidad de Reviews clasificadas como Negativas por el algoritmo de NLP Transformers.
    Positivos:
        Es la cantidad de Reviews clasificadas como Positivas por el algoritmo de NLP Transformers.
    """
    
    result = developer_reviews_analysis(unquote(desarrolladora))
    return result

@app.get("/recommend_games/{item_id}")
def read_recommend_games(item_id: int):
    """
    Endpoint para obtener los 5 juegos recomendados ingresando el id de un juego
    ordenados por puntaje según  matriz de similitud del coseno y 
    la proporción de Reviews clasificadas como Positivas.

    Parámetros:
    -----------
    item_id: int
        Es el ID del juego.

    Devuelve:
    -----------
    Para cada juego recomendado:
    title:
        Es el nombre del juego. 
    item_id:
        Es el id del juego.
    positive_ratio:
        Proporción de Reviews clasificadas como Positivas por el algoritmo de NLP Transformers.    
    similarity_score:
        Score resultante de la matriz de similitud del coseno.
    """
    result = recommend_games(item_id, 5)
    return result