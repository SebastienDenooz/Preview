# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from font_manager.models import File, Thumbnail, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext as _
import json
import mimetypes
import os
import urllib

def Index(request):
    search = None
    if request.GET.get('search'):
        search = request.GET.get('search')
        font_list = File.objects.filter(Q(name__icontains=search)|Q(path__contains=search)|Q(type__contains=search)|Q(note__contains=search)|Q(sha__contains=search)|Q(tags__name__icontains=search)).distinct()
    elif request.GET.get('random'):
        font_list = File.objects.all().order_by("?")[:50]
    else:
        font_list = File.objects.all().distinct()

    paginator = Paginator(font_list, settings.PREVIEWS_BY_PAGE)
    page = request.GET.get('page')
    tags = list(Tag.objects.all().only("name"))

    try:
        fonts = paginator.page(page)
    except PageNotAnInteger:
        fonts = paginator.page(1)
    except EmptyPage:
        fonts = paginator.page(paginator.num_pages)

    return render_to_response('content.html', {'tags': tags, 'fonts': fonts,'total_fonts' : File.objects.all().count(),"search" : search,"demo_text": settings.THUMBNAIL_FORMAT[2][1]},RequestContext(request))


def ViewFile(request,font_id):
    if request.is_ajax():
        return HttpResponse(serializers.serialize("json", [File.objects.get(pk=font_id)]), mimetype="application/json")
    else:
        pass


def GetThumbnail(request,thumbnail_id):
    if request.is_ajax():
        return HttpResponse(serializers.serialize("json", [Thumbnail.objects.get(pk=thumbnail_id)]), mimetype="application/json")
    else:
        pass


def createTag(request,tag_name):
    in_db = Tag.objects.get(name=tag_name)
    if in_db:
        return HttpResponse(_("Tag already created"))
    new_tag = Tag(name=tag_name)
    new_tag.save()
    return HttpResponse(_("Tag successfully created"))


def linkTag(request, _file, tag):
    _file = File.objects.get(pk=_file)
    _tag = Tag.objects.all().filter(name=tag)
    if not _tag:
        tag = Tag(name=tag)
        tag.save()
    else:
        tag = _tag[0]
    _file.tags.add(tag)
    _file.save()
    return HttpResponse(_("Tag successfully added to the file"))


def unlinkTag(request, _file, tag):
    _file = File.objects.get(pk=_file)
    tag = Tag.objects.get(pk=tag)
    _file.tags.remove(tag)
    _file.save()
    return HttpResponse(_("Tag successfully removed from the file"))


def getListOfExistingTags(request):
    tags = Tag.objects.filter(name__icontains=request.GET.get("query"))
    results = {
        "options": []
    }
    for tag in tags:
        results["options"].append(tag.name)
    return HttpResponse(json.dumps(results), mimetype="application/json")

def getFileTags(request, _file):
    _file = File.objects.get(pk=_file)
    tags = list(_file.tags.all().only("id","name"))
    return HttpResponse(serializers.serialize("json", tags), mimetype="application/json")

def getFont(request, sha):
    _file = File.objects.filter(sha=sha)[0]
    fp = open("%s/%s" % (settings.FONT_FILE_PATH, _file.path), 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(_file.path)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat("%s/%s" % (settings.FONT_FILE_PATH, _file.path)).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % _file.name.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(_file.name.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response