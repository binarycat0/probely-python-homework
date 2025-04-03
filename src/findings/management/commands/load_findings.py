import dataclasses
import logging
import os
from argparse import ArgumentParser
from typing import Any

import requests
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)

PROBELY_TOKEN = os.getenv("PROBELY_TOKEN")
PROBELY_TARGET = os.getenv("PROBELY_TARGET")


@dataclasses.dataclass
class ProbelyApi:
    jwt: str
    page_size: int = dataclasses.field(default=10, init=False)
    state: str = dataclasses.field(default="state", init=False)
    host: str = dataclasses.field(default="https://api.probely.com", init=False)

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"JWT {self.jwt}",
        }

    def get_target_findings(self, target_id: str) -> list[dict[str, Any]]:
        results = []

        page = 1
        page_total = 2
        while page <= page_total:
            url = f"{self.host}/targets/{target_id}/findings/"
            params = {"page": page, "length": self.page_size, "": ""}
            result = requests.get(url, headers=self._headers, params=params)
            try:
                result.raise_for_status()
            except Exception as ex:
                logger.error(ex)
                return results

            findings_data = result.json()

            page_total = findings_data.get("page_total")
            page = findings_data.get("page") + 1

            results.append(findings_data.get("results"))

        return results


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "--target",
            type=str,
            required=False,
            help="Pass target_id or value will be taken from PROBELY_TARGET env",
        )
        parser.add_argument(
            "--auth_token",
            type=str,
            required=False,
            help="Pass Probely auth_token or value will be taken from PROBELY_TOKEN env",
        )

    def handle(self, *args, **options):
        target = PROBELY_TARGET or options["target"]
        auth_token = PROBELY_TOKEN or options["auth_token"]
        api = ProbelyApi(auth_token)

        findings = api.get_target_findings(target)
