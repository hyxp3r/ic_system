from api.utils.tandem import Tandem


def test_tandem_get_students():
    tandem = Tandem()
    with tandem:
        results = tandem.get_students()
    assert isinstance(results, list)
    for item in results:
        assert isinstance(item, dict)