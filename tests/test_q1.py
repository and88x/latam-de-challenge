import datetime
from q1_memory import q1_memory
from q1_time import q1_time


def test_q1_format(tmp_path):
    """
    Verifica que la función q1_memory devuelva una lista de tuplas
    con formato (datetime.date, str), como se especifica en la consigna.
    """
    test_file = tmp_path / "test_q1.json"
    test_file.write_text(
        '{"date": "2021-01-01T10:00:00+00:00", "user": {"username": "alice"}}\n'
        '{"date": "2021-01-01T11:00:00+00:00", "user": {"username": "alice"}}\n'
        '{"date": "2021-01-02T12:00:00+00:00", "user": {"username": "bob"}}\n',
        encoding="utf-8",
    )
    result = q1_memory(str(test_file))
    assert isinstance(result, list)
    assert all(
        isinstance(x[0], datetime.date) and isinstance(x[1], str) for x in result
    )


def test_q1_same_output(tmp_path):
    """
    Verifica que q1_memory y q1_time devuelvan el mismo resultado
    cuando se les entrega el mismo archivo.
    """
    test_file = tmp_path / "test_q1.json"
    test_file.write_text(
        '{"date": "2021-01-01T10:00:00+00:00", "user": {"username": "alice"}}\n'
        '{"date": "2021-01-01T11:00:00+00:00", "user": {"username": "alice"}}\n',
        encoding="utf-8",
    )
    assert q1_memory(str(test_file)) == q1_time(str(test_file))
