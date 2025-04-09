import datetime
import heapq

from typing import List, Tuple
from collections import defaultdict
from json import loads as cargar_json


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
        """
    Procesa un archivo de tweets en formato JSON línea por línea, devolviendo las 10 fechas con más
    tweets, junto con el nombre de usuario (username) más activo para cada una de esas fechas.

    Este método está optimizado para un bajo uso de memoria, utilizando un min-heap para mantener
    únicamente las 10 fechas con mayor cantidad de tweets, en lugar de guardar todos los conteos.
    Esto permite reducir significativamente el consumo de memoria en comparación con estrategias
    tradicionales que almacenan el conteo completo de fechas en estructuras grandes.

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
        - El heap mantiene como máximo 10 fechas, descartando automáticamente las menos frecuentes.
    """

    tweets_por_fecha = defaultdict(int)
    tweets_usuario_fecha = defaultdict(lambda: defaultdict(int))

    with open(file_path, "r", encoding="utf-8") as file:
        for linea in file:
            try:
                tweet = cargar_json(linea)

                # Extraer usuario y fecha ("YYYY-MM-DD", 10 dígitos)
                fecha = tweet.get("date", "")[:10]
                usuario = tweet.get("user", {}).get("username", None)

                # Se ignoran los registros incompletos
                if not fecha or not usuario:
                    continue

                # Actualizar contadores
                tweets_por_fecha[fecha] += 1
                tweets_usuario_fecha[fecha][usuario] += 1

            except json.JSONDecodeError:
                continue

    # Usar heap para mantener solo las 10 fechas con más tweets
    heap = []
    for fecha, count in tweets_por_fecha.items():
        heapq.heappush(heap, (count, fecha))
        if len(heap) > 10:
            heapq.heappop(heap)  # elimina la fecha con menos tweets

    # Ordenar fechas de más a menos tweets
    top_fechas = sorted(heap, reverse=True)

    # Usuario más activo de cada fecha
    resultado = []
    for _, fecha in top_fechas:
        usuarios = tweets_usuario_fecha[fecha]
        usuario_mas_activo = max(usuarios.items(), key=lambda x: x[1])[0]
        fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        resultado.append((fecha, usuario_mas_activo))

    return resultado
