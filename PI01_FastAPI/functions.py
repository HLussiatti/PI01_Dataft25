# functions.py
import pandas as pd
import numpy as np
def developer(desarrollador: str):
    
    #Levanto los datos
    df_steam_games = pd.read_parquet('..\\datasets\\3. Depurado y Reducido\\steam_games_dep_reducido.parquet')

    # Verifico si el desarrollador existe en el DataFrame
    if desarrollador.lower() not in df_steam_games['developer'].str.lower().values:
        return f"El desarrollador '{desarrollador}' no se encuentra en el dataset."

    # Filtro por desarrollador
    df_filtered = df_steam_games[df_steam_games['developer'].str.lower()  == desarrollador.lower()]

    # Obtenemos un DF del desarrollador con la cantidad de items por año
    total_items_per_year = df_filtered.groupby('year').size().reset_index(name='total_items')

    # Obtenemos un DF con la cantidad de items "Free" or año
    free_items_per_year = df_filtered[df_filtered['free'] == True].groupby('year').size().reset_index(name='free_items')

    # Left Join de los DF con "year" como clave.
    result = pd.merge(total_items_per_year, free_items_per_year, on='year', how='left').fillna(0)

    # Calculamos el porcentaje de contenido gratuito
    result['percentage_free'] = (result['free_items'] / result['total_items']) * 100

    # Le doy formato a las columnas del DF
    result['year'] = result['year'].astype(int)  # Asegúrate que sea entero
    result['total_items'] = result['total_items'].astype(int)  # Asegúrate que sea entero
    result['free_items'] = result['free_items'].astype(int)    # Asegúrate que sea entero
    result['percentage_free'] = result['percentage_free'].map('{:.2f}%'.format)  # Formato de porcentaje

    # Convertir el DataFrame a una lista de diccionarios (serializable)
    result_json = result.to_dict(orient="records")

    return result_json


def userdata(user_id: str):

    #Levanto los datos
    df_steam_games = pd.read_parquet('..\\datasets\\3. Depurado y Reducido\\steam_games_dep_reducido.parquet')
    df_reviews = pd.read_parquet('..\\datasets\\3. Depurado y Reducido\\user_reviews_NLP.parquet')
    df_user_items = pd.read_parquet('..\\datasets\\2. Depurado\\users_items_depurado.parquet')

    # Me fijo que exista user_id en df_user_items
    if user_id not in df_user_items['user_id'].values:
        return print(f"El user_id {user_id} no se encuentra en user_items.")

    # Filtrar por el user_id en los dataframe
    user_items = df_user_items[df_user_items['user_id'] == user_id]
    user_items = user_items[user_items['item_id'].notnull()]  # Elimino nulos por si quedaron

    # Me fijo que haya items_id en user_items con el user_id
    if user_items.empty:
        print(f"No se encontraron items para el user_id {user_id} en user_items.")
    
    else:
        
        # Obtenemos los items del DF steam_games a partir de los items que tenga el usuario en user:
        items = df_steam_games[df_steam_games['item_id'].isin(user_items['item_id'])]

        if items.empty:
            return print(f"No se encontraron items en steam_games para el user_id {user_id}.")
        else:
            
            #Filtro las reviews del user_id
            user_reviews = df_reviews[(df_reviews['user_id'] == user_id) & (df_reviews['review'].notnull())]
            
            
            # Obtenemos los items del DF steam_games a partir de los items que tenga el usuario en user:
            items = df_steam_games[df_steam_games['item_id'].isin(user_items['item_id'])]
                        
            # Calcular dinero gastado
            total_spent = items['price'].sum()

            # Calcular el porcentaje de recomendación
            if not user_reviews.empty:
                total_reviews = user_reviews['review'].count() # Total de reviews
                recommended_reviews = user_reviews[user_reviews['recommend'] == True]['recommend'].count() # Total de recomendados
                percentage_recommendation = (recommended_reviews / total_reviews) * 100 if total_reviews > 0 else 0 # Porcentaje de recomendados de las reviews. 
            else:
                percentage_recommendation = 0

            # Contar cantidad de items
            item_count = user_items.shape[0]

            # Formatear el resultado
            result = {
                "Usuario": user_id,
                "Dinero gastado": f"{total_spent} USD",
                "% de recomendación": f"{percentage_recommendation:.2f}%",
                "cantidad de items": item_count
            }

            return result
        

def UserForGenre(genero: str):
    # Levantar los datos
    df_steam_games = pd.read_parquet('..\\datasets\\3. Depurado y Reducido\\steam_games_dep_reducido.parquet')
    df_user_items = pd.read_parquet('..\\datasets\\2. Depurado\\users_items_depurado.parquet') 

    # Filtro los juegos por género - genre es un array dentro del DF.
    juegos_genero = df_steam_games[df_steam_games['genres'].apply(lambda x: genero in x if x is not None else False)]

    # Verifico que el género se encuentre en genres
    if juegos_genero.empty:
        return f"No se encontraron juegos para el género '{genero}'."

    # Inner Join de los datos de juegos y tiempo jugado
    user_play_time = pd.merge(df_user_items, juegos_genero[['item_id', 'year']], on='item_id', how='inner')

    # Sumo las horas jugadas por usuario y año
    horas_jugadas = user_play_time.groupby(['user_id', 'year'])['playtime_forever'].sum().reset_index()

    # Calculo el total de horas jugadas por cada usuario para el género
    total_horas_por_usuario = horas_jugadas.groupby('user_id')['playtime_forever'].sum().reset_index()

    # Encontrar el usuario con más horas jugadas
    mejor_usuario = total_horas_por_usuario.loc[total_horas_por_usuario['playtime_forever'].idxmax()]

    # Filtrar las horas jugadas por año para el mejor usuario
    horas_por_año = horas_jugadas[horas_jugadas['user_id'] == mejor_usuario['user_id']]

    # Formatear el resultado
    resultado = {
        "Usuario con más horas jugadas para Género {}".format(genero): mejor_usuario['user_id'],
        "Horas jugadas": [{"Año": int(year), "Horas": int(hours)} for year, hours in zip(horas_por_año['year'], horas_por_año['playtime_forever'])]
    }

    return resultado


def best_developer_year(año: int):
    #Levanto los datos
    df_steam_games = pd.read_parquet('..\\datasets\\3. Depurado y Reducido\\steam_games_dep_reducido.parquet')
    df_reviews = pd.read_parquet('..\\datasets\\3. Depurado y Reducido\\user_reviews_NLP.parquet')
    
    # Filtrar los juegos por año
    juegos_año = df_steam_games[df_steam_games['year'] == año]

    # Verifico si hay juegos en el año dado
    if juegos_año.empty:
        return f"No se encontraron juegos para el año {año}."

    # Filtrar las reviews recomendación "True" y reseñas "Positivas" del NLP
    reseñas_positivas = df_reviews[(df_reviews['recommend'] == True) & (df_reviews['sentiment_value'] == '2')]

    # Verificar si hay reseñas positivas
    if reseñas_positivas.empty:
        return f"No se encontraron reseñas positivas para el año {año}."

    # Inner join de los DF con la columna item_id como id
    juegos_reseñas = pd.merge(juegos_año, reseñas_positivas, on='item_id', how='inner')

    # Verificar si hay reseñas después del merge
    if juegos_reseñas.empty:
        return f"No hay reseñas positivas para los juegos del año {año}."

    # Cuento la cantidad de recomendaciones positivas por desarrollador
    recomendados_por_desarrollador = juegos_reseñas.groupby('developer').size().reset_index(name='count')

    # Obtengo el top 3 desarrolladores (sin ordenar)
    top_desarrolladores = recomendados_por_desarrollador.nlargest(3, 'count')

    # Formatear el resultado en el formato deseado
    resultado = []
    for idx, row in enumerate(top_desarrolladores.itertuples(), start=1):
        puesto = f"Puesto {idx}"
        resultado.append({puesto: row.developer})

    return resultado


def developer_reviews_analysis(desarrolladora: str):

    #Levanto los datos
    df_steam_games = pd.read_parquet('..\\datasets\\3. Depurado y Reducido\steam_games_dep_reducido.parquet')
    df_reviews = pd.read_parquet('..\\datasets\\3. Depurado y Reducido\\user_reviews_NLP.parquet')
    
    
    # Filtrar los juegos del desarrollador especificado. Por las dudas lo paso a minúsculas
    juegos_desarrolladora = df_steam_games[df_steam_games['developer'].str.lower() == desarrolladora.lower()]
    
    # Verifico que haya juegos para este desarrollador y sino devuelvo 0
    if juegos_desarrolladora.empty:
        return {desarrolladora: {'Negative': 0, 'Positive': 0}}

    # Obtener los item_ids de los juegos de la desarrolladora
    item_ids = juegos_desarrolladora['item_id']

    # Filtrar las reseñas relacionadas con esos juegos
    reseñas_desarrolladora = df_reviews[df_reviews['item_id'].isin(item_ids)]

    # Contar las reseñas clasificadas como positivas y negativas
    total_positivas = reseñas_desarrolladora[reseñas_desarrolladora['sentiment_value'] == '2'].shape[0]
    total_negativas = reseñas_desarrolladora[reseñas_desarrolladora['sentiment_value'] == '0'].shape[0]

    # Crear el diccionario de resultados
    resultado = {
        desarrolladora: {
            'Negative': int(total_negativas),
            'Positive': int(total_positivas)
        }
    }

    return resultado
