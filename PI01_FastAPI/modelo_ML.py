# modelo_ML.py
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import gc

def release_resources(*dfs):
    """
    Elimina las variables pasadas como argumento y fuerza la recolección de basura.
    :param dfs: DataFranes cargadis a eliminar.
    """
    for var in dfs:
        del var
    gc.collect()


def matrix_calculation(item_id,df_steam_games):
    
    # Vectorizo la columna combinada usando TF-IDF y creo la matriz
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df_steam_games['combined'])

    # Busco el índice del juego (índice de DF) y guardo por separado el vector del juego y los demás por separado (incluido él mismo)
    idx = df_steam_games.index[df_steam_games['item_id'] == item_id].tolist()[0]
    game_vector = tfidf_matrix[idx]
    other_games_vector = tfidf_matrix

    # Calculo la matriz de similitud del coseno
    cosine_sim = cosine_similarity(game_vector, other_games_vector).flatten()
    
    # Elimino el índice del juego consigo mismo 
    cosine_sim[idx] = 0

    # Devuelvo el resultado
    release_resources(df_steam_games)
    return cosine_sim


# Función para recomendar juegos
def recommend_games(item_id, n_recommendations):
    
    #Cargo los datos para verificar que exista el id en primer lugar
    df_steam_games = pd.read_parquet('../datasets/2. Depurado/steam_games_postEDA.parquet', columns=['item_id', 'title', 'positive_ratio','combined'])
    df_steam_games.reset_index(drop=True, inplace=True)
    
    # Verifico que exista el id del juego.
    if df_steam_games[df_steam_games['item_id'] == item_id].empty:
        release_resources(df_steam_games)
        return f"El item_id {item_id} no existe en el dataset."

    # Se debe calcular la matriz SOLO para el item_id, sino la matriz es demasiado grande para calcularla o para caragarla.
    cosine_sim = matrix_calculation(item_id,df_steam_games)

    # Ordeno por los valores de la similitud
    sim_scores = list(enumerate(cosine_sim))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Tomo los n primeros valores
    sim_scores = sim_scores[0:n_recommendations]  

    # Extraigo los índice y los puntajes de los "n_recommendations" juegos recomendados
    game_indices = [i[0] for i in sim_scores[:n_recommendations]]
    game_sim_scores = [i[1] for i in sim_scores]

    # Retornar los juegos recomendados junto con los puntajes de similitud
    recommended_games = df_steam_games.loc[df_steam_games.index.isin(game_indices), ['item_id', 'title', 'positive_ratio']]
    recommended_games['similarity_score'] = game_sim_scores
    recommended_games['similarity_score'] = recommended_games['similarity_score'].round(4)

    # Como puede haber varios juegos con igual puntaje, decido ordenarlos por el posiive_ratio resultante del NLP
    recommended_games = recommended_games.sort_values(by='positive_ratio', ascending=False)

    # Como puede ocurrir que haya valore nulos, tengo que reemplazarlos sino después no puedo pasrlos a json en Render
    recommended_games.fillna(value=0, inplace=True) 

    # Convertir el DataFrame a una lista de diccionarios (serializable)
    result_json = recommended_games.to_dict(orient="records")

    release_resources(df_steam_games)
    return result_json