import json
from typing import Any

import pytest
import os
from probely.clients.probely import ProbelyApi, ProbelyApiException


@pytest.fixture(scope="module")
def api() -> ProbelyApi:
    return ProbelyApi("test")


@pytest.fixture
def target_id() -> str:
    return "target_id"


@pytest.fixture
def mock_response() -> dict[str, Any]:
    f = open(
        os.path.join(os.path.dirname(__file__), "fixtures/findings_response.json"), "r"
    )
    return json.load(f)


class TestProbelyApiClient:

    def test_get__ok(self, mocker, mock_response, api, target_id):
        result = mocker.MagicMock()
        result.raise_for_status = mocker.MagicMock(return_value=True)
        result.json = mocker.MagicMock(return_value=mock_response)

        mocker.patch("requests.get", return_value=result)
        findings = api.get_target_findings(target_id)

        assert findings
        assert len(findings) == 2

    def test_get__error(self, mocker, api, target_id):
        with pytest.raises(ProbelyApiException) as ex:
            mocker.patch("requests.get", side_effect=Exception("test"))
            api.get_target_findings(target_id)

        assert ex
