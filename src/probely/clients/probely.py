import dataclasses
import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


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
