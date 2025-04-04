from unittest import TestCase

import pytest

from probely.clients.probely import ProbelyApi


@pytest.fixture(scope="module")
def api() -> ProbelyApi:
    return ProbelyApi("test")


@pytest.fixture(scope="session")
def target_id() -> str:
    return "target_id"


def test_get__ok(api, target_id):

    result = api.get_target_findings(target_id)
