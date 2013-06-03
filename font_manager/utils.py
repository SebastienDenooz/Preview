import magic
import os
import Image, ImageFont, ImageDraw
from django.conf import settings
from font_manager.models import Thumbnail
import string
import sys
import math
import logging

logger = logging.getLogger(__name__)

__author__ = 'sebastien'

FONT_FORMATS = (
    # ('File ext', 'MimeType')
    ('.eot', 'application/vnd.ms-fontobject'),
    ('.pfb', 'application/octet-stream'),
    ('.ttf', 'application/x-font-ttf'),
    ('.pfm', 'application/octet-stream'),
    ('.fon', 'application/x-dosexec'),
    ('.woff', 'application/octet-stream'),
    ('.svg', 'image/svg+xml'),
)


def isFontFile(path):

    DirName, Extension = os.path.splitext(path)
    try:
        Mimetype = magic.from_file(path, mime=True)
    except:
        logger.error("ERROR : %s" % sys.exc_info()[0])
        return False

    if (Extension, Mimetype) not in FONT_FORMATS:
        return False
    else:
        return True


def GenerateThumbnailImages(file):

    DirName, Extension = os.path.splitext(file)
    target_dir = file.replace(settings.FONT_FILE_PATH+"/","")

    if not os.path.isdir(settings.THUMBNAIL_FILE_PATH+"/"+target_dir):
        os.makedirs(settings.THUMBNAIL_FILE_PATH+"/"+target_dir)
    files = []
    # FIXME : Not working for pfm, fon, eot, woff, svg font file...
    if isFontFile(file) and (Extension not in (".pfm", ".fon", ".eot", ".woff", ".svg")):
        for thumb_format in settings.THUMBNAIL_FORMAT:
            lines = string.split(thumb_format[1],"\n")
            nb_char = 0
            biger_line = ""
            for line in lines:
                if len(line) > nb_char:
                    biger_line = line
                    nb_char = nb_char
            font = ImageFont.truetype(file, 75)

            x = y = None
            if  font.getsize(biger_line)[0] < 1:
                x = 20
            else:
                x = font.getsize(biger_line)[0]

            if (font.getsize(biger_line)[1])*len(lines) < 1:
                y = 20*len(lines)
            else:
                y =  (font.getsize(biger_line)[1])*len(lines)


            font_size =  (x,y)
            thumbnail = Image.new(
                "RGBA",
                font_size,
                (255,255,255)
            )
            height=0
            for line in lines:
                draw = ImageDraw.Draw(thumbnail)
                draw.text(
                    (0, height),
                    line.decode('utf-8'),
                    (0,0,0),
                    font=font
                )
                height = height+font.getsize(biger_line)[1]
            thumbnail.thumbnail((thumb_format[2],thumb_format[3]), Image.ANTIALIAS)
            thumbnail.save(settings.THUMBNAIL_FILE_PATH+"/"+target_dir+"/"+os.path.basename(file)+"."+thumb_format[0]+".png")
            files.append((thumb_format[0],target_dir+"/"+os.path.basename(file)+"."+thumb_format[0]+".png"))

    return files


def CreateThumbnail(file,sha):
    thumbnail_images = GenerateThumbnailImages(file)
    thumbnail_obj = []
    for thumbnail_image in thumbnail_images:
        thumbnail = Thumbnail(
            name = thumbnail_image[0],
            path = thumbnail_image[1],
            source = 0,
            sha=sha
        )
        thumbnail.save()
        thumbnail_obj.append(thumbnail)
        thumbnail.save()
    return thumbnail_obj