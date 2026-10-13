import pytest
from shopper_composite import db_connector


'''
@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
    ],
)
'''
def test_get_config():
    result = db_connector.get_config("/home/lcalleja/shopper_composite/secrets.yaml")
    assert result['host'] == 'localhost'

def test_connect():
    with db_connector.connect() as conn:
        assert conn is not None
        assert conn.is_connected()
        