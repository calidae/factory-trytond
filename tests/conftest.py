import pytest

from trytond.pool import Pool


@pytest.fixture
def pool(transaction):
    return Pool()
