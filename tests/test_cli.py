import pytest
from shopper_composite import cli

def test_cli_main():
    result = cli.main()
    assert result is not None
    assert isinstance(result, str)