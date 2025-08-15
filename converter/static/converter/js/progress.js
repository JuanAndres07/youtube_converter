document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const downloadAudioForm = document.getElementById('download-audio-form');
    const downloadVideoForm = document.getElementById('download-video-form');
    const searchLoading = document.getElementById('search-loading');

    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            if (searchLoading) {
                searchLoading.style.display = 'block';
            }
        });
    }

    const showDownloadModal = () => {
        Swal.fire({
            title: 'Convirtiendo...',
            text: 'Por favor, espera mientras se convierte el video.',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
    }

    if (downloadAudioForm) {
        downloadAudioForm.addEventListener('submit', showDownloadModal)
    }

    if (downloadVideoForm) {
        downloadVideoForm.addEventListener('submit', showDownloadModal)
    }

    const filename = document.body.dataset.filename;

    if (filename) {
        Swal.fire({
            icon: 'success',
            title: 'Descarga completa',
            text: `El archivo ${filename} se ha convertido correctamente.`,
            confirmButtonText: 'Descargar',
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = `/download/${filename}`;
                history.replaceState(null, '', '/');
            }
        });
    }
});