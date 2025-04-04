from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from findings.models import Finding


class FindingModelTest(TestCase):
    def setUp(self):
        self.scans = [{"scan_id": 1, "status": "complete"}]
        self.finding = Finding.objects.create(
            url="https://example.com",
            path="/api/data",
            method="GET",
            target_id="T123",
            definition_id="D456",
            scans=self.scans,
        )

    def test_finding_creation(self):
        self.assertEqual(self.finding.url, "https://example.com")
        self.assertEqual(self.finding.path, "/api/data")
        self.assertEqual(self.finding.method, "GET")
        self.assertEqual(self.finding.target_id, "T123")
        self.assertEqual(self.finding.definition_id, "D456")
        self.assertIsInstance(self.finding.scans, list)
        self.assertEqual(self.finding.scans, self.scans)

    def test_blank_target_and_definition(self):
        finding = Finding.objects.create(
            url="https://test.com", path="/health", method="POST"
        )
        self.assertEqual(finding.target_id, "")
        self.assertEqual(finding.definition_id, "")
        self.assertEqual(finding.scans, [])


class FindingViewTest(APITestCase):
    def setUp(self):
        self.finding1 = Finding.objects.create(
            url="https://example.com/1",
            path="/v1/test",
            method="GET",
            target_id="T001",
            definition_id="D001",
            scans=["scan-a", "scan-b"],
        )
        self.finding2 = Finding.objects.create(
            url="https://example.com/2",
            path="/v1/test",
            method="POST",
            target_id="T002",
            definition_id="D002",
            scans=["scan-b", "scan-c"],
        )

    def test_list_findings(self):
        url = reverse("finding-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_id(self):
        url = reverse("finding-list")
        response = self.client.get(url, {"id": self.finding1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.finding1.id)

    def test_filter_by_target_id(self):
        url = reverse("finding-list")
        response = self.client.get(url, {"target_id": "T002"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["target_id"], "T002")

    def test_filter_by_definition_id(self):
        url = reverse("finding-list")
        response = self.client.get(url, {"definition_id": "D001"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["definition_id"], "D001")

    def test_filter_by_scans(self):
        url = reverse("finding-list")
        response = self.client.get(url, {"scans": ["scan-a"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.finding1.id)

    def test_retrieve_finding(self):
        url = reverse("finding-detail", args=[self.finding2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.finding2.id)
