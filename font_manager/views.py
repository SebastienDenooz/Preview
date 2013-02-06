# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from font_manager.models import File, Thumbnail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings

def Index(request):
    search = None
    if request.GET.get('search'):
        search = request.GET.get('search')
        font_list = File.objects.filter(Q(name__contains=search)|Q(path__contains=search)|Q(type__contains=search)|Q(note__contains=search)|Q(sha__contains=search)).distinct()
    elif request.GET.get('random'):
        font_list = File.objects.all().order_by("?")[:50]
    else:
        font_list = File.objects.all().distinct()


    paginator = Paginator(font_list, settings.PREVIEWS_BY_PAGE)
    page = request.GET.get('page')
    try:
        fonts = paginator.page(page)
    except PageNotAnInteger:
        fonts = paginator.page(1)
    except EmptyPage:
        fonts = paginator.page(paginator.num_pages)
    return render_to_response('content.html', {'fonts': fonts,'total_fonts' : File.objects.all().count(),"search" : search,"demo_text": settings.THUMBNAIL_FORMAT[2][1]},RequestContext(request))


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
