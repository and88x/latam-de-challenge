from q3_memory import q3_memory
from q3_time import q3_time


def test_q3_format(tmp_path):
    """
    Verifica que q3_memory devuelva una lista de tuplas (username, cantidad),
    con tipos correctos: str e int.
    """
    test_file = tmp_path / "test_q3.json"
    test_file.write_text(
        '{"mentionedUsers": [{"username": "alice"}]}\n'
        '{"mentionedUsers": [{"username": "bob"}, {"username": "alice"}]}\n',
        encoding="utf-8",
    )
    result = q3_memory(str(test_file))
    assert isinstance(result, list)
    assert all(isinstance(u, str) and isinstance(c, int) for u, c in result)


def test_q3_same_output(tmp_path):
    """
    Verifica que q3_memory y q3_time devuelvan el mismo resultado
    con un archivo que contiene menciones simples.
    """
    test_file = tmp_path / "test_q3.json"
    test_file.write_text(
        '{"mentionedUsers": [{"username": "alice"}]}\n', encoding="utf-8"
    )
    assert q3_memory(str(test_file)) == q3_time(str(test_file))
