from django.db import models


# Create your models here.
class Finding(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=255)


class Scans(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    findings = models.ManyToManyField(Finding, related_name="scans")


class Target(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    findings = models.ManyToManyField(Finding, related_name="targets")


class Definition(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField()
    desc = models.CharField()
    findings = models.ManyToManyField(Finding, related_name="definitions")
