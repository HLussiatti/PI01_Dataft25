# functions.py
import pandas as pd
import gc

def release_resources(*dfs):
    """
    Elimina las variables pasadas como argumento y fuerza la recolección de basura.
    :param dfs: DataFranes cargadis a eliminar.
    """
    for var in dfs:
        del var
    gc.collect()


def developer(desarrollador: str):
    #Levanto los datos necesarios
    df_steam_games = pd.read_parquet('../datasets/2. Depurado/steam_games_depurado.parquet', columns=['developer','year','free'])

    # Verifico si el desarrollador existe en el DataFrame
    if desarrollador.lower() not in df_steam_games['developer'].str.lower().values:
        release_resources(df_steam_games)
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

    release_resources(df_steam_games)
    return result_json


def userdata(user_id: str):

    #Levanto los datos
    df_steam_games = pd.read_parquet('../datasets/2. Depurado/steam_games_depurado.parquet', columns=['item_id','price'])
    df_reviews = pd.read_parquet('../datasets/2. Depurado/user_reviews_NLP_Transformers.parquet', columns=['user_id','item_id','review','recommend'])
    df_user_items = pd.read_parquet('../datasets/2. Depurado/users_items_depurado.parquet', columns=['user_id','item_id'])

    # Me fijo que exista user_id en df_user_items
    if user_id not in df_user_items['user_id'].values:
        release_resources(df_steam_games, df_reviews,df_user_items)
        return f"El user_id {user_id} no se encuentra en user_items."

    # Filtrar por el user_id en los dataframe
    user_items = df_user_items[df_user_items['user_id'] == user_id]
    user_items = user_items[user_items['item_id'].notnull()]  # Elimino nulos por si quedaron

    # Me fijo que haya items_id en user_items con el user_id
    if user_items.empty:
        release_resources(df_steam_games, df_reviews,df_user_items)
        return f"No se encontraron items para el user_id {user_id} en user_items."
    
    else:
        
        # Obtenemos los items del DF steam_games a partir de los items que tenga el usuario en user:
        items = df_steam_games[df_steam_games['item_id'].isin(user_items['item_id'])]

        if items.empty:
            release_resources(df_steam_games, df_reviews,df_user_items)
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
            
            release_resources(df_steam_games, df_reviews,df_user_items)
            return result
        

def UserForGenre(genero: str):
    # Levantar los datos
    df_steam_games = pd.read_parquet('../datasets/2. Depurado/steam_games_depurado.parquet', columns=['genres','item_id','year'])
    df_user_items = pd.read_parquet('../datasets/2. Depurado/users_items_depurado.parquet', columns=['user_id','item_id','playtime_forever']) 

    # Filtro los juegos por género - genre es un array dentro del DF.
    games_genres = df_steam_games[df_steam_games['genres'].apply(lambda x: genero in x if x is not None else False)]

    # Verifico que el género se encuentre en genres
    if games_genres.empty:
        release_resources(df_steam_games,df_user_items)
        return f"No se encontraron juegos para el género '{genero}'."

    # Inner Join de los datos de juegos y tiempo jugado
    user_play_time = pd.merge(df_user_items, games_genres[['item_id', 'year']], on='item_id', how='inner')

    # Sumo los minutos jugados por usuario y año
    play_time = user_play_time.groupby(['user_id', 'year'])['playtime_forever'].sum().reset_index()

    # Convierto los minutos a horas
    play_time['playtime_forever'] = play_time['playtime_forever'] / 60

    # Calculo el total de horas jugadas por cada usuario para el género
    total_user_play_time = play_time.groupby('user_id')['playtime_forever'].sum().reset_index()

    # Encontrar el usuario con más horas jugadas
    max_total_user_play_time = total_user_play_time.loc[total_user_play_time['playtime_forever'].idxmax()]

    # Filtrar las horas jugadas por año para el mejor usuario
    play_time_by_year = play_time[play_time['user_id'] == max_total_user_play_time['user_id']]

    # Formatear el resultado
    result = {
        "Usuario con más horas jugadas para Género {}".format(genero): max_total_user_play_time['user_id'],
        "Horas jugadas": [{"Año": int(year), "Horas": int(hours)} for year, hours in zip(play_time_by_year['year'], play_time_by_year['playtime_forever'])]
    }

    release_resources(df_steam_games,df_user_items)
    return result


def best_developer_year(año: int):
    #Levanto los datos
    df_steam_games = pd.read_parquet('../datasets/2. Depurado/steam_games_depurado.parquet', columns=['item_id','year','developer'])
    df_reviews = pd.read_parquet('../datasets/2. Depurado/user_reviews_NLP_Transformers.parquet', columns=['user_id','item_id','recommend','sentiment_value'])
    
    # Filtrar los juegos por año
    games_years = df_steam_games[df_steam_games['year'] == año]

    # Verifico si hay juegos en el año dado
    if games_years.empty:
        release_resources(df_steam_games,df_reviews)
        return f"No se encontraron juegos para el año {año}."

    # Filtrar las reviews recomendación "True" y reseñas "Positivas" del NLP
    positive_reviews = df_reviews[(df_reviews['recommend'] == True) & (df_reviews['sentiment_value'] == '2')]

    # Verifico si hay reseñas positivas
    if positive_reviews.empty:
        release_resources(df_steam_games,df_reviews)
        return f"No se encontraron reseñas positivas para el año {año}."

    # Left join de los DF con la columna item_id como id
    games_reviews = pd.merge(games_years, positive_reviews, on='item_id', how='left')

    # Verifico si hay reseñas después del merge
    if games_reviews.empty:
        release_resources(df_steam_games,df_reviews)
        return f"No hay reseñas positivas para los juegos del año {año}."

    # Cuento la cantidad de recomendaciones positivas por desarrollador
    positive_reviews_by_developer = games_reviews.groupby('developer').size().reset_index(name='count')

    # Obtengo el top 3 desarrolladores (sin ordenar)
    top_developers = positive_reviews_by_developer.nlargest(3, 'count')

    # Formatear el resultado en el formato deseado
    result = []
    for idx, row in enumerate(top_developers.itertuples(), start=1):
        puesto = f"Puesto {idx}"
        result.append({puesto: row.developer})

    release_resources(df_steam_games,df_reviews)
    return result


def developer_reviews_analysis(desarrolladora: str):

    #Levanto los datos
    df_steam_games = pd.read_parquet('../datasets/2. Depurado/steam_games_depurado.parquet',columns=['item_id','developer'])
    df_reviews = pd.read_parquet('../datasets/2. Depurado/user_reviews_NLP_Transformers.parquet',columns=['item_id','sentiment_value'])
    
    
    # Filtrar los juegos del desarrollador especificado. Por las dudas lo paso a minúsculas
    games_by_developer = df_steam_games[df_steam_games['developer'].str.lower() == desarrolladora.lower()]
    
    # Verifico que haya juegos para este desarrollador y sino devuelvo 0
    if games_by_developer.empty:
        release_resources(df_steam_games,df_reviews) 
        return {desarrolladora: {'Negativos': 0, 'Positivos': 0}}

    # Obtener los item_ids de los juegos de la desarrolladora
    item_ids = games_by_developer['item_id']

    # Filtrar las reseñas relacionadas con esos juegos
    reviews_by_developer = df_reviews[df_reviews['item_id'].isin(item_ids)]

    # Contar las reseñas clasificadas como positivas y negativas resultantes del NLP
    total_positives = reviews_by_developer[reviews_by_developer['sentiment_value'] == '2'].shape[0]
    total_negatives = reviews_by_developer[reviews_by_developer['sentiment_value'] == '0'].shape[0]

    # Crear el diccionario de resultados
    result = {
        desarrolladora: {
            'Negativos': int(total_positives),
            'Positivos': int(total_negatives)
        }
    }

    release_resources(df_steam_games,df_reviews) 
    return result
