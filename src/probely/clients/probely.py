import dataclasses
import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


class ProbelyApiException(Exception): ...


@dataclasses.dataclass
class ProbelyApi:
    jwt: str
    page_size: int = dataclasses.field(default=10, init=False)
    host: str = dataclasses.field(default="https://api.probely.com", init=False)

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"JWT {self.jwt}",
        }

    def get_target_findings(self, target_id: str) -> list[dict[str, Any]]:
        results = []

        url = f"{self.host}/targets/{target_id}/findings/"
        page = 1
        page_total = 2
        while page <= page_total:
            params = {"page": page, "length": self.page_size, "state": "notfixed"}
            try:
                result = requests.get(url, headers=self._headers, params=params)
                result.raise_for_status()
            except Exception as ex:
                logger.error(ex)
                raise ProbelyApiException(str(ex)) from ex

            findings_data = result.json()

            page_total = findings_data.get("page_total")
            page = findings_data.get("page") + 1

            results.extend(findings_data.get("results"))

        return results
