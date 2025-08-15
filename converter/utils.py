from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from urllib.parse import urlparse, parse_qs
import subprocess
import os

def get_video_info(url: str) -> dict:
    """ 
    Obtiene informacion del video sin descargarlo
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = info.get('formats', [])
        video_formats = []

        for f in formats:
            """ if f.get('url') and f.get('vcodec') != 'none' and f.get('height'): """
            """  and f.get('acodec') != 'none' """

            if f.get('url') and f.get('vcodec') != 'none' and f.get('ext') == 'mp4' and f.get('acodec') != 'none' :
                resolution = f"{f.get('height', '?')}p"
                video_formats.append({
                    'format_id': f.get('format_id'),
                    'resolution': resolution,
                    'filesize': f.get('filesize', 0),
                    'ext': f.get('ext'),
                    'tbr': f.get('tbr', 0),                         # Taza de bits
                })    

        best_by_resolution = {}
        for vf in video_formats:
            res = vf['resolution']
            if res not in best_by_resolution or vf['tbr'] > best_by_resolution[res]['tbr']:
                best_by_resolution[res] = vf

        return {
            'title': info.get('title', 'Sin Titulo'),
            'thumbnail': info.get('thumbnail'),
            'duration': info.get('duration', 0),
            'video_formats': list(best_by_resolution.values()),
        }
    
    except Exception as e:
        return {}


def download_mp3(url: str) -> str:
    """ 
    Descarga solo el audio como MP3
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'media/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    
    filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
    return filename


def download_custom_video(url: str, video_format_id: str) -> str:
    """ 
    Descarga video en formato MP4 con un ID de formato especifico
    """
    output_template = 'media/%(title)s.%(ext)s'

    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = info.get('formats', [])
        selected_format = next((f for f in formats if f.get('format_id') == video_format_id), None)

        if not selected_format:
            raise ValueError(f"Formato con ID {video_format_id} no encontrado para este video.")
    
        needs_aac_conversion = False
        
        if selected_format.get('acodec') != 'none':

            if selected_format.get('acodec') != 'aac':
                needs_aac_conversion = True

            format_str = video_format_id
        else:
            format_str = f"{video_format_id}+bestaudio/best"
            needs_aac_conversion = True

        ydl_opts = {
            'format': format_str,
            'merge_output_format': 'mp4',
            'outtmpl': output_template,
            'quiet': True,
            'yt_client': 'android',
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)

        if needs_aac_conversion:
            filepath = convert_audio_to_aac(filepath)

        return filepath
    
    except DownloadError as e:
        raise ValueError(f"No se pudo descargar el video: {e}")
    
    except Exception as e:
        raise ValueError(f"Error al descargar el video: {e}")
    

def convert_audio_to_aac(filepath: str, ffmpeg_path: str = r'C:\ffmpeg\bin\ffmpeg.exe') -> str:
    """ 
    Convierte el audio de un archivo de video a AAC usando ffmpeg.
    """
    base_name, ext = os.path.splitext(filepath)
    output_path = base_name + '_aac' + ext

    subprocess.run([
        ffmpeg_path, '-i', filepath,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_path
    ], check=True)

    os.remove(filepath)
    return output_path


def clean_url(url: str) -> str:
    """ 
    Limpia la URL de posibles parametros innecesarios
    """
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    video_id = query.get('v')

    if video_id:
        return f"https://www.youtube.com/watch?v={video_id[0]}"
    
    return url