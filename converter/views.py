import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import FileResponse, Http404
from django.contrib import messages
from .forms import DownloadForm ,DownloadMP4Form, DownloadMP3Form
from .utils import download_custom_video, download_mp3, get_video_info, clean_url

def index(request):
    filename = request.GET.get('filename')
    video_data = None
    video_formats = []
    select_format = None
    cleaned_url = None
    mp3_form = None
    mp4_form = None

    if request.method == 'POST':
        form = DownloadForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['url']
            select_format = form.cleaned_data['format']

            cleaned_url = clean_url(url)
            video_data = get_video_info(cleaned_url)

            if not video_data:
                messages.error(request, "No se pudo obtener la información del video. Verifica la URL e intenta nuevamente.")
            else:
                if select_format == 'mp4':
                    video_formats = video_data.get('video_formats', [])
                    mp4_form = DownloadMP4Form(initial={'url': cleaned_url})

                elif select_format == 'mp3':
                    mp3_form = DownloadMP3Form(initial={'url': cleaned_url})
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = DownloadForm()

    return render(request, 'converter/index.html', {
        'form': form,
        'video_data': video_data,
        'video_formats': video_formats,
        'select_format': select_format,
        'filename': filename,
        'cleaned_url': cleaned_url,
        'mp3_form':mp3_form,
        'mp4_form': mp4_form
    })

def download_video(request):
    if request.method == 'POST':
        form = DownloadMP4Form(request.POST)
        if form.is_valid():
            url = clean_url(form.cleaned_data['url'])
            format_id = form.cleaned_data['video_format_id']

            try:
                filepath = download_custom_video(url, format_id)
                filename = os.path.basename(filepath)
                return redirect(f'/?filename={filename}')
            
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('/')
    return redirect("/")
        
def download_audio(request):
    if request.method == 'POST':
        form = DownloadMP3Form(request.POST)
        if form.is_valid():
            url = clean_url(form.cleaned_data['url'])
            filepath = download_mp3(url)
            filename = os.path.basename(filepath)

            return redirect(f'/?filename={filename}')
    
    return redirect('/')

def download_file(request, filename):
    filepath = os.path.join(settings.BASE_DIR, 'media', filename)

    if os.path.exists(filepath):
        response = FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)
        return response
    
    else:
        raise Http404("Archivo no encontrado")