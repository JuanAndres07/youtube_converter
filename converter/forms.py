from django import forms
import re

class DownloadForm(forms.Form):
    url = forms.URLField(
        label='URL del video',
        max_length=2000,
        widget=forms.URLInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Ingresa la URL del video',
        }),
        error_messages={
            'required': 'Este campo es obligatorio.',
            'invalid': 'Por favor, ingresa una URL válida.',
        }
    )

    format = forms.ChoiceField(
        choices=[('mp3', 'MP3'), ('mp4', 'MP4')],
        label='Formato de descarga',
        widget=forms.RadioSelect,
        error_messages={
            'required': 'Debes seleccionar un formato de descarga.',
        }
    )

    """ Funcion para validar URL ingresada """
    def clean_url(self):
        url = self.cleaned_data['url']

        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
        )

        if not youtube_regex.match(url):
            raise forms.ValidationError("La URL ingresada no es válida. Debe ser un enlace de YouTube.")
        return url
    
class DownloadMP3Form(forms.Form):
    url = forms.URLField(widget=forms.HiddenInput())
    format = forms.CharField(widget=forms.HiddenInput(), initial='mp3')

class DownloadMP4Form(forms.Form):
    url = forms.URLField(widget=forms.HiddenInput())
    format = forms.CharField(widget=forms.HiddenInput(), initial='mp4')
    
    video_format_id = forms.CharField(required=True)