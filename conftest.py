"""
Global pytest fixtures, accesibles desde cualquier test.
"""

import pytest


@pytest.fixture(autouse=True)
def _enable_db_for_all_tests(db):
    """
    Habilita acceso a la BD para todos los tests automáticamente.
    Sin esto tendrías que poner @pytest.mark.django_db en cada test.
    """
    pass
