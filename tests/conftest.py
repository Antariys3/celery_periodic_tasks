from decimal import Decimal
from unittest.mock import patch, Mock
import json

import pytest
from django.core.management import call_command

from exchange.models import Rate


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "rates.json")
