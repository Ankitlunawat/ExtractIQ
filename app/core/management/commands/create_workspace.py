import os
from django.core.management.base import BaseCommand,CommandError
from django.contrib.auth.models import User
class Command(BaseCommand):
    def handle(self,*args,**options):
        password=os.environ.get("LOCAL_PASSWORD")
        if not password:raise CommandError("Set LOCAL_PASSWORD first.")
        user,created=User.objects.get_or_create(username="workspace")
        if created:user.set_password(password);user.save()
        self.stdout.write("Workspace ready; existing credentials unchanged.")
