from pathlib import Path
from django.core.management.base import BaseCommand,CommandError
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from core.models import ExtractionJob,ExtractedRecord
from core.scraper import crawl
class Command(BaseCommand):
    help="Extract the approved practice catalogue, with retries and validation."
    def add_arguments(self,p):
        p.add_argument("--user",default="workspace")
        p.add_argument("--pages",type=int,default=2)
        p.add_argument("--cache",default=None)
    def handle(self,*args,**options):
        try:user=User.objects.get(username=options["user"])
        except User.DoesNotExist:raise CommandError("Create the local workspace first.")
        job=ExtractionJob.objects.create(owner=user,name="Catalogue extraction",state="running")
        try:
            rows,metrics=crawl(options["pages"],options["cache"])
            with transaction.atomic():
                ExtractedRecord.objects.bulk_create([ExtractedRecord(job=job,**r) for r in rows])
                for k,v in metrics.items():setattr(job,k,v)
                job.state="completed";job.finished_at=timezone.now();job.save()
            self.stdout.write(f"Completed: {len(rows)} unique records; {metrics}")
        except Exception as exc:
            job.state="failed";job.error=str(exc);job.finished_at=timezone.now();job.save()
            raise CommandError(str(exc))
