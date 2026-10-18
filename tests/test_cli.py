import pytest
from shopper_composite import cli

def test_cli_main():
    result = cli.main()
    print(f'number of rows written: {result}')
    assert result is not None
    assert isinstance(result, int)