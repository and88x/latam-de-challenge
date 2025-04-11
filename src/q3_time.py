import re

from typing import List, Tuple
from collections import Counter
from json import loads as cargar_json, JSONDecodeError


def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo de tweets en formato JSON línea por línea, devolviendo los 10 usuarios
    más mencionados (en el campo 'mentionedUsers') a lo largo de todo el historial.

    Esta versión está optimizada para minimizar el tiempo de ejecución. En lugar de parsear
    todas las líneas del archivo, utiliza una expresión regular para detectar solo aquellas
    líneas que contienen al menos un usuario mencionado, reduciendo significativamente la
    cantidad de operaciones costosas de json.loads().

    Args:
        file_path (str): Ruta al archivo de tweets en formato JSON (una línea por tweet).

    Returns:
        List[Tuple[str, int]]:
            Una lista ordenada (descendente) con los 10 usuarios más mencionados.
            Cada elemento es una tupla que contiene:
                - str: El username del usuario mencionado.
                - int: Cantidad total de veces que fue mencionado.

            Ejemplo:
            [
                ("LATAM321", 387),
                ("LATAM_CHI", 129),
                ...
            ]

    Notas y supuestos:
        - Se asume que cada línea del archivo representa un JSON válido con codificación UTF-8.
        - Solo se procesan las líneas que contienen una lista con al menos un objeto dentro del
          campo 'mentionedUsers'.
        - Las líneas sin menciones o con arrays vacíos se descartan automáticamente antes de parsear
          el JSON.
        - Tweets mal formateados son ignorados.
    """

    menciones = Counter()
    patron = re.compile(r'"mentionedUsers":\s*\[\s*{')

    with open(file_path, "r", encoding="utf-8") as file:
        for linea in file:
            if not patron.search(linea):
                continue  # descarta líneas sin usuarios mencionados

            try:
                tweet = cargar_json(linea)
                for usuarios_mencionados in tweet.get("mentionedUsers") or []:
                    usuario = usuarios_mencionados.get("username")
                    if usuario:
                        menciones[usuario] += 1

            except JSONDecodeError:
                continue

    return menciones.most_common(10)
