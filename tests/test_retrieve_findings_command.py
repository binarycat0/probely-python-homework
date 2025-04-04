import pytest
from django.core.management import call_command
from findings.models import Finding


@pytest.mark.django_db
def test_retrieve_findings_command(mocker):
    mock_api = mocker.patch("findings.management.commands.retrieve_findings.ProbelyApi")
    mock_api.return_value.get_target_findings.return_value = [
        {
            "url": "https://example.com",
            "path": "/login",
            "method": "GET",
            "target": {"id": "T001"},
            "definition": {"id": "D001"},
            "scans": ["scan-1", "scan-2"],
        }
    ]

    call_command("retrieve_findings", "--target", "T001", "--auth_token", "dummy-token")

    assert Finding.objects.count() == 1
    finding = Finding.objects.first()
    assert finding.url == "https://example.com"
    assert finding.target_id == "T001"
    assert finding.definition_id == "D001"
    assert finding.scans == ["scan-1", "scan-2"]
