from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse

# Librerias del modelo machin learning
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("plataformas.csv", usecols=['id', 'type', 'title', 'cast', 'country',
                 'release_year', 'rating', 'listed_in', 'duration_int', 'duration_type', 'scored'])
df2 = pd.read_csv("ML.csv")

app = FastAPI()

# @app.get lo que hace es regristrar la funcion
# uvicorn main:app --reload para correr la fastApi. El reload hace que si hago un cambio solamente actualizando la pagina ya guarda todo
# /docs para que en el https: me muestre las funciones
# http://127.0.0.1:8000/


@app.get("/get_max_duration/{year}/{platform}/{duration_type}")
def get_max_duration(year: int, platform: str, duration_type: str):

    # Voy a indicarle en plataforma que me interesa la primer letra que es como le indique a la hora de crearlo para cada plataforma. (Ej:Netflix = n)
    # Tambien si el usuario ingresa en mayuscula que lo cambie a minuscula
    duration_type = duration_type.lower()
    platfrom = platform.lower()[0]

    # Filtro por año de lanzamiento y por plataforma. Que tenga encuentra la primer letra de id
    data = df[(df["release_year"] == year) & (df["id"].str.startswith(platfrom)) & (
        df["duration_type"] == duration_type) & (df["type"] == "movie")]

    # En la condicion voy a indicar tanto la palabra en ingles como español
    if duration_type == "min" or duration_type == "duration" or duration_type == "duracion":
        # Filtro por duracion y que devuelva todos los datos
        df_duration = data[data["duration_type"] == duration_type]
        max_duration = df_duration["duration_int"].max()
        max_duration_data = df_duration.loc[df_duration["duration_int"]
                                            == max_duration]

    # En este caso lo mismo, indico tanto el ingreso en ingles como español
    elif duration_type == "seasons" or duration_type == "temporada":
        df_duration = data[data["duration_type"] == duration_type]
        max_duration = df_duration["duration_int"].max()
        max_duration_data = df_duration.loc[df_duration["duration_int"]
                                            == max_duration]

    # Selecciono el primer registro de max_duration_date y obtengo el titulo que cumplen la condicion
    title_pelicula = max_duration_data.iloc[0]["title"]

    # Retorno el titulo de la pelicula con mayor duracion. Ya que en max_duration_data tenia toda la informacion de esa pelicula y solo me pedia devolver el titulo
    return {"pelicula": title_pelicula}


@app.get("/get_score_count/{platform}/{scored}/{year}")
def get_score_count(platform: str, scored: float, year: int) -> int:

    # Convierto a minúsculas y obtengo la primera letra de la plataforma
    platform = platform.lower()[0]

    # Filtro el df para que sea pelicula solamente,
    # selecciono todas las filas que tienen el valor de id que comienza con la letra que representa la plataforma(startswith)
    # Que el valor sea mayor al de scored
    # Y el año de la pelicula que se paso en la funcion
    df_filtrado = df.loc[(df["type"] == "movie") & (df["id"].str.startswith(
        platform)) & (df["scored"] > scored) & (df["release_year"] == year)]
    resultado = len(df_filtrado)
    # Necesite hacer el JSONResponse porque el dato de algunas variables que no pueden ser almacenado o transmitido por ellos es neceario transformarlo a formato JSON
    # Que es el formato que utiliza fastApi
    return JSONResponse(content={"plataforma": platform, "cantidad": resultado, "anio": year, "score": scored})


@app.get("/get_count_platform/{platform}")
def get_count_platform(platform):
    # Como anteriormente me voy a asegurar que lo que se ingrese lo pase a minusculas
    platform = platform.lower()
    platform = platform.lower()[0]
    # filtro
    df_filtrado = df.loc[(df["type"] == "movie") & (
        df["id"].str.startswith(platform))]
    # Ahora cuento la cantidad de filas del df_filtrado con las condiciones y selecciono el primer elemento
    count = df_filtrado.shape[0]
    return {"plataforma": platform, "peliculas": count}


@app.get("/get_actor/{platform}/{year}")
def get_actor(platform: str, year: int):

    # Filtro por plataforma y año
    platform = platform.lower()[0]
    data = df[(df["id"].str.startswith(platform)) & (
        df["release_year"] == year) & (df["type"] == "movie")]

    # filtro una lista con todos los actores
    # Utilizo flatten para obtener un array de numpy unidimensional con todos los valores.
    # De esta manera, obtengo una lista de todos los actores presentes en el dataframe, sin importar en qué columna aparezcan.
    actores = data["cast"].str.split(", ", expand=True).values.flatten()

    # Compruebo si la lista de actores está vacía O tenemos valores en NaN. Si esta condicion se cumple devuelvo "no hay datos".
    if actores.size == 0 or pd.isnull(actores).all():
        return "no hay datos"

    # Contar la cantidad de veces que aparece cada actor
    cantidad_actores = pd.Series(actores).value_counts()

    # Obtener el actor más repetido
    top_actor, top_count = cantidad_actores.idxmax(), cantidad_actores.max()

    # Devuelvo el actor que mas se repitio por plataforma y la cantidad de veces que aparecio.
    # A top_count lo paso a int para que lo tome la fast api
    return {"plataform": platform, "anio": year, "actor": top_actor, "cantidad": int(top_count)}


@app.get("/prod_per_country/{tipo}/{pais}/{anio}")
def prod_per_country(tipo: str, pais: str, anio: int):
    # Filtro por tipo de contenido, país y año.
    data = df[(df["type"] == tipo.lower()) & (
        df["country"] == pais) & (df["release_year"] == anio)]

    # Agrupo los datos por país, año y tipo de contenido, y cuento la cantidad de productos en cada grupo.
    # Un count del grupo para que me cuente la cantidad de veces que aparece cada combinacion unica de las 3 columnas
    # Reset_index elimino el indice actual y lo reemplazo por una secuencia numerica para hacer mas facil contarlos
    cantidad_producto = data.groupby(["country", "release_year", "type"]).count()[
        "id"].reset_index()

    # Accedo al valor de la columna id de la primera fila del df can tidad_producto. Y despues si la cantidad es mayor a 0 muestro la cantidad si no 0.
    resultado = int(cantidad_producto.iloc[0]["id"]) if len(
        cantidad_producto) > 0 else 0

    return {"Pais": pais, "Anio": anio, "Peliculas": resultado}


@app.get("/get_contents/{rating}")
def get_contents(rating: str):

    # Filtro por rating de audiencia.
    data = df[df["rating"] == rating]

    # Cuento la cantidad de productos que cumplen con la condición.
    numero_contents = len(data)

    return {"Recomendacion": numero_contents}


@app.get("/get_recommendation/{title}")
def get_recommendation(title: str):
    title = title.lower()
    # Obtengo la fila correspondiente a la pelicula de interes
    peliculas_idx = df2[df2["title"] == title].index[0]
    # Creo una instancia de TfidfVectorizer y creo la matriz de frecuencia de términos
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df2["listed_in"])
    # Calculo la similitud del coseno
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    # Obtengo las peliculas por similitud
    peliculas_similares = list(enumerate(cosine_sim[peliculas_idx]))
    # Ordeno las peliculas por similitud
    agregar_peliculas = sorted(
        peliculas_similares, key=lambda x: x[1], reverse=True)
    # Obtengo los indices de las 5 peliculas mas similares
    top_similar = [i[0] for i in agregar_peliculas[1:6]]
    # Obtengo los nombres de las pelicualas mas similares
    top_similares_titulos = df2["title"].iloc[top_similar]
    # Obtengo los scores de las peliculas mas similares
    top_similares_score = [agregar_peliculas[i][1] for i in top_similar]
    # Obtengo las peliculas similares y a la ves que presentan mayor score
    # Zip toma dos iterables y los combia en una lista de tuplas en este caso los 2 escores
    # Desempaqueto las tuplas en la lista ordenada, donde _ representa la variable score y x el titulo.
    peliculas_recomendadas = [x for _, x in sorted(
        zip(top_similares_score, top_similares_titulos), reverse=True)][:5]

    return {"titulo": peliculas_recomendadas}
