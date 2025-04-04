from rest_framework.fields import IntegerField, CharField, JSONField
from rest_framework.serializers import ModelSerializer

from findings.models import Finding


class FindingSerializer(ModelSerializer):
    id = IntegerField()
    url = CharField()
    path = CharField()
    method = CharField()

    target_id = CharField()
    definition_id = CharField()
    scans = JSONField()

    class Meta:
        model = Finding
        fields = ["id", "url", "path", "method", "target_id", "definition_id", "scans"]
