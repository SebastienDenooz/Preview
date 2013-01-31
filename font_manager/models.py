from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    name = models.CharField(_("Name"),max_length=128)

class Vote(models.Model):
    sha = models.TextField(_("SHA Sum"))
    score = models.IntegerField(_("Score"),max_length=1)
    user = models.ForeignKey(User)

class Thumbnail(models.Model):
    path = models.FilePathField(_("Path to the tiny thumbNail"))
    name = models.CharField(_("Name"),max_length=255)
    sha = models.TextField(_("Hash of the file"))
    """
    source : it can be :
    0 : Automatically created
    100 : Uploaded by an anonymous
    200 : Uploaded by a user
    """
    source = models.IntegerField(_("Source of the cache"))

class File(models.Model):
    path = models.FilePathField(_("Path"))
    sha = models.TextField(_("SHA Sum"))
    name = models.CharField(_("Name"),max_length=255)
    tags = models.ManyToManyField(Tag)
    type = models.CharField(_("File type"),max_length=255)
    note = models.TextField(_("Notes"))
    thumbnails = models.ManyToManyField(Thumbnail)
