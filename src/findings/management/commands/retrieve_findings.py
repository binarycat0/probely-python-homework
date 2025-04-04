import logging
import os
from argparse import ArgumentParser

from django.core.management import BaseCommand

from findings.models import Finding
from probely.clients.probely import ProbelyApi, ProbelyApiException

logger = logging.getLogger(__name__)

PROBELY_TOKEN = os.getenv("PROBELY_TOKEN")
PROBELY_TARGET = os.getenv("PROBELY_TARGET")


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

        try:
            target_findings = api.get_target_findings(target)
        except ProbelyApiException:
            logger.error(
                "Something went wrong while retrieving Findings from Probely. Check logs."
            )
            return

        Finding.objects.bulk_create(
            [
                Finding(
                    url=f.get("url"),
                    path=f.get("path"),
                    method=f.get("method"),
                    target_id=f.get("target", {}).get("id"),
                    definition_id=f.get("definition", {}).get("id"),
                    scans=f.get("scans"),
                )
                for f in target_findings
            ]
        )
