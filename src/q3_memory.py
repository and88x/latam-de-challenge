from typing import List, Tuple
from collections import Counter
from json import loads as cargar_json, JSONDecodeError


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo de tweets en formato JSON línea por línea, devolviendo los 10 usuarios
    más influyentes, definidos como aquellos que más veces fueron mencionados (@username).

    Este método está optimizado para un bajo uso de memoria, ya que no carga el archivo completo
    en memoria, sino que procesa cada tweet individualmente a través de un generador que produce
    los usernames mencionados uno por uno. Luego utiliza un Counter para acumular las menciones.

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
        - Se asume que cada línea del archivo es un JSON válido con codificación UTF-8.
        - El campo 'mentionedUsers' puede ser nulo, omitido o una lista vacía.
        - Se ignoran los tweets mal formateados o sin menciones válidas.
    """

    def generador_menciones():
        """
        Generador que produce los nombres de usuario mencionados (username)
        en el campo 'mentionedUsers' de cada tweet válido del archivo.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            for linea in file:
                try:
                    tweet = cargar_json(linea)

                    for usuarios_mencionados in tweet.get("mentionedUsers") or []:
                        usuario = usuarios_mencionados.get("username")
                        if usuario:
                            yield usuario

                except JSONDecodeError:
                    continue

    menciones = Counter()
    menciones.update(generador_menciones())
    return menciones.most_common(10)
