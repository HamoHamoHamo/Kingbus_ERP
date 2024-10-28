import os
from uuid import uuid4
from django.views.generic import CreateView, DetailView
from django.shortcuts import render, get_object_or_404
from config.settings.base import MEDIA_ROOT, BASE_DIR, MEDIA_URL
from firebase.media_firebase import download_file


class FileViewerMixin(DetailView):
    template_name = "file_viewer.html"
    # model = 

    def get(self, request, file_id):
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')
        
        file = get_object_or_404(self.model, id=file_id)
        # 파일 경로 = tmp/테이블명+id

        splited_filename = file.filename.split(".")
        is_pdf = True if splited_filename[len(splited_filename) - 1] == "pdf" else False
        
        file_destination = f"tmp/{self.model.__name__}_{file.id}"
        local_destination = os.path.join(MEDIA_ROOT, file_destination)

        if not os.path.isfile(local_destination):
            download_file(file.path, local_destination)

        context = {
            'url' : os.path.join(MEDIA_URL, file_destination),
            'is_pdf' : is_pdf,
        }
        return render(request, 'file_viewer.html', context)