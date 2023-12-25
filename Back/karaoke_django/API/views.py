import os
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
import sys
directorio_padre = os.path.dirname(os.path.abspath(__file__))
sys.path.append(directorio_padre)
from services.Karaoke import funcion_completa


# Create your views here.


class index(TemplateView):
    template_name = 'API/index.html'
    


def get_video(request):
    title = request.GET.get('title', '')
    if title == '':
        return HttpResponse(status=400)
    funcion_completa(title)
    video_file_path = os.path.join(settings.MEDIA_ROOT, 'videos', 'output.mp4')
    return FileResponse(open(video_file_path, 'rb'), content_type='video/mp4')
