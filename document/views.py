import urllib
import os
import mimetypes
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from ERP.settings import BASE_DIR

from .models import Document, DocumentFile
from .forms import DocumentForm
from crudmember.models import User

from datetime import datetime, timedelta

# Create your views here.
class DocumentList(generic.ListView):
    template_name = 'document/document_list.html'
    context_object_name = 'document_list'
    paginate_by = 10
    model = Document

    def get_queryset(self):
        document_list = Document.objects.order_by('-id')
        return document_list
    # 페이징 처리
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        #페이징 끝
        return context

class DocumentDetail(generic.DetailView):
    template_name = 'document/document_detail.html'
    context_object_name = 'document'
    model = Document

    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context를 가져온다.
        context = super(DocumentDetail, self).get_context_data(**kwargs)
        context['document_files'] = DocumentFile.objects.filter(document_id=self.kwargs['pk'])
        return context

def download(request, pk, file_id):
    download_file = get_object_or_404(DocumentFile, pk=file_id)
    url = download_file.file.url
    root = str(BASE_DIR)+url
    print("\n테스트\n", root)

    if os.path.exists(root):
        with open(root, 'rb') as fh:
            quote_file_url = urllib.parse.quote(download_file.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404
    else:
        print("에러")
        raise Http404

def document_create(request):
    context = {}
    if request.method == "POST":
        creator = get_object_or_404(User, pk=request.session.get('user'))
        document_form = DocumentForm(request.POST)
        if document_form.is_valid():
            files = request.FILES.getlist('file', None)
            document = document_form.save(commit=False)
            document.creator = creator
            document.save()
            document_file_save(files, document)
            return redirect('document:document_list')
    else:
        context = {
            'document_form' : DocumentForm(),
        }
    return render(request, 'document/document_create.html', context)

def document_file_save(upload_file, document):
    for file in upload_file:
        document_file = DocumentFile(
            document_id=document,
            file=file,
            filename=file.name,
        )
        document_file.save()
    return

def document_edit(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document_files = DocumentFile.objects.filter(document_id=pk)

    if request.method == 'POST':
         if User.objects.get(pk=request.session['user']).authority == "관리자":
            creator = get_object_or_404(User, pk=request.session.get('user'))
            document_form = DocumentForm(request.POST)
            edit_files = request.FILES.getlist('file', None)
            if document_form.is_valid():
                edit_document = document_form.save(commit=False)
                document.title = edit_document.title
                document.content = edit_document.content        
                document.creator = creator
                document.save()

                document_file_save(edit_files, document)
            return redirect(reverse('document:document_detail', args=(pk,)))
    else:
        context = {
            'document' : document,
            'document_form' : DocumentForm(instance=document),
            'document_files' : DocumentFile.objects.filter(document_id=document)
        }
    return render(request, 'document/document_edit.html', context)

def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document_file = document.document_file.all()
    if User.objects.get(pk=request.session['user']).authority == "관리자":
        if document_file:
            for file in document_file:
                os.remove(file.file.path)
        document.delete()
    return redirect('document:document_list')

def file_delete(request, pk, file_id):
    document = get_object_or_404(Document, pk=pk)
    document_file = DocumentFile.objects.get(pk=file_id)
    os.remove(document_file.file.path)
    document_file.delete()
    
    context = {
        'document' : document,
        'document_form' : DocumentForm(instance=document),
        'document_files' : DocumentFile.objects.filter(document_id=document),
    }
    return redirect(reverse('document:document_edit', args=(pk,)))

