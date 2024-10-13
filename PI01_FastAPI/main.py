# app.py

import pandas as pd
import numpy as np
import uvicorn
from fastapi import FastAPI
from urllib.parse import unquote
from functions import developer
from functions import userdata
from functions import UserForGenre
from functions import best_developer_year
from functions import developer_reviews_analysis

app = FastAPI()


@app.get("/developer/{desarrolladora}")
def read_developer_reviews(desarrolladora: str):
    """
    Endpoint para obtener la cantidad de items y porcentaje 
    de contenido Free por año según empresa desarrolladora.
    :param desarrolladora: Es la desarrolladora del Juego .
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
    el porcentaje de recomendación en base a reviews.recommend y cantidad de items.
    :param user_id: Es el identificador único del usuario. 
    """
    resultado = userdata(unquote(user_id))
    return resultado

@app.get("/UserForGenre/{genero}")
def read_UserForGenre(genero: str):
    """
    Endpoint para obtener el usuario que acumula más horas jugadas para 
    el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.
    """
    resultado = UserForGenre(unquote(genero))
    return resultado

@app.get("/best_developer_year/{anio}" )
def read_best_developer_year(anio: int):
    """
    Endpoint para obtener el top 3 de desarrolladores con juegos MÁS recomendados 
    por usuarios para el año dado. (reviews.recommend = True y comentarios positivos).
    """
    resultado = best_developer_year(anio)
    return resultado

@app.get("/developer_reviews_analysis/{desarrolladora}")
def read_developer_reviews_analysis(desarrolladora: str):
    """
    Endpoint para obtener un diccionario con el nombre del desarrollador 
    como llave y una lista con la cantidad total de registros de reseñas de 
    suarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo..
    """
    resultado = developer_reviews_analysis(unquote(desarrolladora))
    return resultado