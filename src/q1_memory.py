import datetime

from json import loads as cargar_json
from typing import List, Tuple
from collections import Counter, defaultdict


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Procesa un archivo de tweets en formato JSON línea por línea, devolviendo las 10 fechas con más
    tweets, junto con el nombre de usuario (username) más activo para cada una de esas fechas.

    Este método está optimizado para un bajo uso de memoria, ya que no carga todo el archivo en
    memoria, sino que procesa cada tweet individualmente y solo guarda conteos incrementales.

    Args:
        file_path (str): Ruta al archivo de tweets en formato JSON (una línea por cada tweet).

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
        - Se asume que cada línea del archivo es un JSON válido.
        - La fecha debe estar en el campo "date" con formato ISO 8601 (ej: "2021-02-24T09:23:35+00:00").
        - El username se encuentra en el campo "user.username".
        - Tweets sin fecha o usuario válido se ignoran.
    """

    tweets_por_fecha = Counter()
    tweets_usuario_fecha = defaultdict(Counter)

    with open(file_path, "r", encoding="utf-8") as file:
        for linea in file:
            tweet = cargar_json(linea)

            # Extraer usuario y fecha ("YYYY-MM-DD", 10 dígitos)
            usuario = tweet.get("user", {}).get("username", None)
            fecha = tweet.get("date", "")[:10]

            # Se ignoran los registros incompletos
            if not fecha or not usuario:
                continue

            # Convertir a objeto datetime.date
            fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()

            # Actualizar contadores
            tweets_por_fecha[fecha] += 1
            tweets_usuario_fecha[fecha][usuario] += 1

    # Obtener 10 fechas con más tweets ordenadas de mayor a menor
    top_fechas = tweets_por_fecha.most_common(10)

    # Usuario más activo de cada fecha
    resultado = []
    for fecha, _ in top_fechas:
        usuario_mas_activo, _ = tweets_usuario_fecha[fecha].most_common(1)[0]
        resultado.append((fecha, usuario_mas_activo))

    return resultado
