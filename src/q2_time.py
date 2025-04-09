from emoji import EMOJI_DATA
from typing import List, Tuple
from collections import Counter
from json import loads as cargar_json, JSONDecodeError


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo de tweets en formato JSON cargándolo completamente en memoria,
    y devuelve los 10 emojis más utilizados junto con su cantidad de ocurrencias.

    Este método está optimizado para velocidad de ejecución, ya que evita la lectura
    línea por línea (I/O secuencial) y utiliza estructuras eficientes como `set` para
    búsquedas rápidas y `Counter` para acumulación directa.

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
        - Se asume que cada línea del archivo es un JSON válido codificado en UTF-8.
        - El campo de texto a procesar se encuentra en "content".
        - La detección de emojis se realiza carácter por carácter, comparando con un conjunto (`set`)
          construido a partir de `emoji.EMOJI_DATA.keys()`, que contiene todos los emojis reconocidos.
        - Tweets sin campo "content" o vacíos se ignoran.
    """

    emoji_set = set(EMOJI_DATA.keys())
    conteo_de_emojis = Counter()

    with open(file_path, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    for linea in lineas:
        try:
            tweet = cargar_json(linea)
            contenido_del_tweet = tweet.get("content", "")

            for caracter in contenido_del_tweet:
                if caracter in emoji_set:
                    conteo_de_emojis[caracter] += 1

        except JSONDecodeError:
            continue

    return conteo_de_emojis.most_common(10)
