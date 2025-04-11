from emoji import is_emoji
from typing import List, Tuple
from collections import Counter
from json import loads as cargar_json, JSONDecodeError


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo de tweets en formato JSON línea por línea, devolviendo los 10 emojis más utilizados
    junto con su cantidad de ocurrencias.

    Este método está optimizado para un bajo uso de memoria, ya que no carga todo el archivo en
    memoria, sino que procesa cada tweet individualmente y realiza conteo_de_emojiss incrementales de emojis
    directamente sobre el texto, sin almacenar datos intermedios.

    Args:
        file_path (str): Ruta al archivo de tweets en formato JSON (una línea por cada tweet).

    Returns:
        List[Tuple[str, int]]:
            Una lista ordenada (descendente) con los 10 emojis más frecuentes y su cantidad de apariciones.
            Cada elemento es una tupla que contiene:
                - str: Emoji.
                - int: Número total de veces que el emoji aparece en los tweets.

            Ejemplo:
            [
                ("✈️", 6856),
                ("❤️", 5876),
                ...
            ]

    Notas y supuestos:
        - Se asume que cada línea del archivo es un JSON válido.
        - El texto a procesar se encuentra en el campo "content" de cada tweet.
        - Los emojis son identificados carácter por carácter utilizando la función emoji.is_emoji().
        - Tweets sin campo "content" o vacíos se ignoran.
    """

    conteo_de_emojis = {}

    with open(file_path, "r", encoding="utf-8") as file:
        for linea in file:
            try:
                tweet = cargar_json(linea)
                contenido_del_tweet = tweet.get("content", "")

                for caracter in contenido_del_tweet:
                    if is_emoji(caracter):
                        conteo_de_emojis[caracter] = (
                            conteo_de_emojis.get(caracter, 0) + 1
                        )

            except JSONDecodeError:
                continue

    # Obtener el top 10 de emojis más usados
    top_10 = sorted(conteo_de_emojis.items(), key=lambda x: x[1], reverse=True)[:10]
    return top_10
