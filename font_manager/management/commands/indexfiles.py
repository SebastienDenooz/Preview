from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from font_manager.models import File
from font_manager.utils import isFontFile
import os
import magic
import hashlib

class Command(BaseCommand):
    help = "Register files in the database"

    def handle(self, *args, **options):

        newly_indexed = []
        indexed_files = File.objects.all().values_list('path', flat=True)

        for root, dirs, files in os.walk(settings.FONT_FILE_PATH):
            for file in files:
                if isFontFile(root+"/"+file):
                    path = root.replace(settings.FONT_FILE_PATH,"")+"/"+file
                    if (path not in indexed_files) and (path not in newly_indexed):
                        new_file = File(
                            path=path,
                                sha=hashlib.sha1(open(root+'/'+file,'rb').read()).hexdigest(),
                            name=file,
                            type=magic.from_file(root+'/'+file, mime=True),
                        )
                        new_file.save()
                        newly_indexed.append(path)
                        print "Add "+path
