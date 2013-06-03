from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from font_manager.models import File, Directory
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Register files in the database"

    def handle(self, *args, **options):

        for root, dirs, files in os.walk(settings.FONT_FILE_PATH):
            for dir in dirs:
                directory_path = "%s/%s" %(root,dir)
                in_db = Directory.objects.filter(path=directory_path).count()
                if not in_db:
                    new_path = Directory(
                        path=directory_path,
                        status=0,
                        last_update=None
                    )
                    new_path.save()
                    logger.info("Adding %s" %(directory_path))