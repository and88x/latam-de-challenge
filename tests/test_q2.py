from q2_memory import q2_memory
from q2_time import q2_time


def test_q2_format(tmp_path):
    """
    Verifica que la salida de q2_memory sea una lista de tuplas
    (emoji, conteo), donde emoji es str y conteo es int.
    """
    test_file = tmp_path / "test_q2.json"
    test_file.write_text(
        '{"content": "✈️❤️🔥"}\n' '{"content": "🔥🔥✈️"}\n', encoding="utf-8"
    )
    result = q2_memory(str(test_file))
    assert isinstance(result, list)
    assert all(isinstance(e, str) and isinstance(c, int) for e, c in result)


def test_q2_same_output(tmp_path):
    """
    Verifica que q2_memory y q2_time devuelvan el mismo resultado
    ante un input controlado.
    """
    test_file = tmp_path / "test_q2.json"
    test_file.write_text('{"content": "❤️❤️✈️"}\n', encoding="utf-8")
    assert q2_memory(str(test_file)) == q2_time(str(test_file))
