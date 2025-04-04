from django.db import models


class Finding(models.Model):
    objects: models.Manager

    id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=255)

    target_id = models.CharField(max_length=20, blank=True)
    definition_id = models.CharField(max_length=20, blank=True)
    scans = models.JSONField(null=True, default=list)
