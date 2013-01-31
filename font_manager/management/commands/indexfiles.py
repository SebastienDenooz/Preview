from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from font_manager.models import File
from font_manager.utils import isFontFile
import os
import magic
import hashlib


def processDirectory ( args, dirname, filenames ):
    for filename in filenames:
        file_path = (dirname+'/'+filename).replace(settings.FONT_FILE_PATH,"")
        if isFontFile(dirname+'/'+filename):
            print dirname+'/'+filename
            search_file = File.objects.filter(path=file_path)
            if search_file.count() == 0:
                sha = hashlib.sha1(open(dirname+'/'+filename,'rb').read()).hexdigest()
#                thumb_files = Thumbnail.objects.filter(sha=sha)
#                if thumb_files.count() == 0 :
#                    thumb_files = CreateThumbnail(dirname+'/'+filename,sha)
                new_file = File(
                    path=file_path,
                    sha=sha,
                    name=filename,
                    type=magic.from_file(dirname+'/'+filename, mime=True),
                )
                new_file.save()
#                new_file.thumbnails.add(*thumb_files)
                print "Add ",sha
            else:
                #print "."
                pass


class Command(BaseCommand):
    #   args = "<all>"
    help = "Register files in the database"

    def handle(self, *args, **options):
        os.path.walk(settings.FONT_FILE_PATH, processDirectory, None )