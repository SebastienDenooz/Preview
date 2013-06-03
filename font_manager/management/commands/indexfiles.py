from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from datetime import datetime, timedelta
from font_manager.models import File, Directory
from font_manager.utils import isFontFile
from os import listdir
import magic
import hashlib
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

NEW = 0
INDEXING = 1
INDEXED = 2

class Command(BaseCommand):
    help = "Register files in the database"

    def handle(self, *args, **options):
        time_threshold = datetime.now() - timedelta(seconds=settings.UPDATE_FREQUENCY)
        directory_to_index = Directory.objects.filter(Q(last_update__lt=(time_threshold)) | Q(last_update=None) | Q(status=INDEXING)).order_by('?')[0]
        file_added = 0
        while file_added < settings.MINIMUM_NUMBER_FILES_TO_INDEX or not directory_to_index:
            file_path = directory_to_index.path
            directory_to_index.status = INDEXING
            directory_to_index.save()
            for file in listdir(file_path):
                if isFontFile("%s/%s" % (file_path, file)):
                    sha_sum = hashlib.sha1(open(file_path+'/'+file,'rb').read()).hexdigest()
                    file_in_db = File.objects.filter(path=file_path.replace(settings.FONT_FILE_PATH, '')).filter(name=file)
                    if not file_in_db:
                        new_file = File(
                            path="%s/%s" % (file_path.replace(settings.FONT_FILE_PATH, ""), file),
                            sha=sha_sum,
                            name=file,
                            type=magic.from_file(file_path+'/'+file, mime=True),
                        )
                        new_file.save()
                        file_added += 1
                        logger.info("Add %s/%s" % (file_path, file))
            directory_to_index.last_update = datetime.now()
            directory_to_index.status = INDEXED
            directory_to_index.save()
            directory_to_index = Directory.objects.filter(Q(last_update__lt=(time_threshold)) | Q(last_update=None)).order_by('?')[0]
        logger.info( "%s file(s) added" % file_added)
