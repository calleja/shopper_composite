import pytest
import shopper_composite.cli as cli


def test_logger():
    assert cli.logger is not None