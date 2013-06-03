from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.conf import settings
from font_manager.models import File, Thumbnail
from font_manager.utils import GenerateThumbnailImages,CreateThumbnail
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--create',
            action='store_true',
            dest='create',
            default=False,
            help='The sha sum of the file'
        ),
        make_option('--sha',
            action='store_true',
            dest='sha',
            default=False,
            help='The sha sum of the file'
        ),
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete thumbnail of the given sha'
        ),
        make_option('--update',
            action='store_true',
            dest='update',
            default=False,
            help='update thumbnail of the given sha'
        ),
    )
    args = "<sha max_thumbnails>"
    help = "Register files in the database"


    def handle(self, *args, **options):
        if len(options) == 0:
            logger.error("No option given. Read help with ./manage.py help thumbnails")
        else:
            file_list = None
            if not options['sha']:
                file_list = File.objects.filter(thumbnails=None).distinct()[0:settings.THUMBNAIL_CREATED_BY_PASS]
            else:
                if options["delete"]:
                    file_list = File.objects.filter(sha=options["sha"])
                elif options['update']:
                    file_list = File.objects.filter(sha=options["sha"])
                else:
                    logger.error("Use --update or --delete with sha option. More infos with ./manage.py help thumbnails")

            for file in file_list:
                thumb_files = Thumbnail.objects.filter(sha=file.sha)

                if options["delete"]:
                    for thumb in thumb_files:
                        os.remove(settings.THUMBNAIL_FILE_PATH+"/"+thumb.path)
                        thumb.delete()
                elif options["update"]:
                    if thumb_files.count() > 0 :
                        for thumb in thumb_files:
                            os.remove(settings.THUMBNAIL_FILE_PATH+"/"+thumb.path)
                            thumb.delete()
                    thumb_files = CreateThumbnail(settings.FONT_FILE_PATH+'/'+file.path,file.sha)
                    file.thumbnails.append(thumb_files)
                    file.save()
                else:
                    if thumb_files.count() > 0 :
                        for thumb in thumb_files:
                            os.remove(settings.THUMBNAIL_FILE_PATH+"/"+thumb.path)
                            thumb.delete()
                    thumb_files = CreateThumbnail(settings.FONT_FILE_PATH+'/'+file.path,file.sha)
                    file.thumbnails.add(*thumb_files)
                    file.save()
                    logger.info("Add thumb for"+file.sha)