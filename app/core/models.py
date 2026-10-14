from django.db import models
from django.conf import settings

class ExtractionJob(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(max_length=140)
    source=models.URLField(default="https://books.toscrape.com/")
    state=models.CharField(max_length=15,default="pending")
    pages=models.PositiveIntegerField(default=0)
    duplicates=models.PositiveIntegerField(default=0)
    rejected=models.PositiveIntegerField(default=0)
    error=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    finished_at=models.DateTimeField(null=True)

class ExtractedRecord(models.Model):
    job=models.ForeignKey(ExtractionJob,on_delete=models.CASCADE,related_name="records")
    title=models.CharField(max_length=400)
    url=models.URLField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    currency=models.CharField(max_length=3,default="GBP")
    rating=models.PositiveIntegerField()
    available=models.BooleanField()
    fingerprint=models.CharField(max_length=64)
    class Meta:
        constraints=[models.UniqueConstraint(fields=["job","fingerprint"],name="one_record_per_job")]
