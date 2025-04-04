from django.db.models.query import RawQuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet

from findings.models import Finding
from findings.serializers import FindingSerializer


class FindingView(ReadOnlyModelViewSet):
    serializer_class = FindingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "target_id", "definition_id"]

    def _filter_by_scans_sqlite(self, scans: list[str]) -> RawQuerySet:
        condition = " OR ".join(f"json_each.value = '{scan}'" for scan in scans)
        query = f"""
            SELECT id FROM findings_finding ff
            WHERE EXISTS (SELECT 1 FROM json_each(ff.scans) WHERE {condition})
        """
        return Finding.objects.raw(query)

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)

    def get_queryset(self):
        scans = self.request.query_params.getlist("scans")
        if scans:
            data = self._filter_by_scans_sqlite(scans)
            return Finding.objects.filter(id__in=[d.id for d in data])

        return Finding.objects.all()

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
