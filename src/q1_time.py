import datetime

from typing import List, Tuple
from json import loads as cargar_json
from collections import Counter, defaultdict


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Procesa un archivo de tweets en formato JSON cargándolo completamente en memoria, devolviendo las
    10 fechas con más tweets, junto con el nombre de usuario (username) más activo para cada una de esas
    fechas.

    Este método está optimizado para minimizar el tiempo de ejecución, cargando el archivo completo en
    memoria para reducir operaciones de I/O. Las estructuras utilizadas (`Counter` y `defaultdict`)
    permiten realizar conteos y agrupaciones de manera eficiente directamente en memoria.

    Args:
        file_path (str): Ruta al archivo de tweets en formato JSON (una línea por cada tweet, codificado
        en UTF-8).

    Returns:
        List[Tuple[datetime.date, str]]:
            Una lista ordenada (descendente) con las 10 fechas con más tweets.
            Cada elemento es una tupla que contiene:
                - datetime.date: La fecha específica.
                - str: Nombre de usuario con más tweets ese día.

            Ejemplo:
            [
                (datetime.date(2021, 2, 24), "LATAM321"),
                (datetime.date(2021, 2, 23), "otroUsuario"),
                ...
            ]

    Notas y supuestos:
        - El archivo debe estar codificado como UTF-8 y cada línea debe contener un JSON válido.
        - El campo "date" debe tener formato ISO 8601 (ej: "2021-02-24T09:23:35+00:00").
        - El nombre de usuario se encuentra en el campo "user.username".
        - Tweets sin fecha o sin username válido son ignorados.
    """

    tweets_por_fecha = Counter()
    tweets_usuario_fecha = defaultdict(Counter)

    # Leer todo el archivo a memoria para reducir I/O
    with open(file_path, "rb") as file:
        lineas = file.readlines()

    for linea in lineas:
        try:
            tweet = cargar_json(linea)

            # Extraer usuario y fecha ("YYYY-MM-DD", 10 dígitos)
            fecha = tweet.get("date", "")[:10]
            usuario = tweet.get("user", {}).get("username")

            # Se ignoran los registros incompletos
            if not fecha or not usuario:
                continue

            # Actualizar contadores
            tweets_por_fecha[fecha] += 1
            tweets_usuario_fecha[fecha][usuario] += 1

        except orjson.JSONDecodeError:
            continue

    # Obtener top 10 fechas en orden descendente
    top_fechas = tweets_por_fecha.most_common(10)

    # Usuario más activo de cada fecha
    resultado = []
    for fecha, _ in top_fechas:
        usuario_top = tweets_usuario_fecha[fecha].most_common(1)[0][0]
        fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        resultado.append((fecha, usuario_top))

    return resultado
