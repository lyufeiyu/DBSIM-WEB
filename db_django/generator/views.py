from django.shortcuts import render

# Create your views here.
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings

@csrf_exempt
def file_upload(request):
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()    # 请注意，我们使用了 FileSystemStorage 类来保存上传的文件。该类会将文件保存在由 MEDIA_ROOT 设置定义的位置。
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # 这里可以调用你的数据处理函数，比如:
        # process_file(os.path.join(settings.MEDIA_ROOT, filename))

        return JsonResponse({'status': 'success', 'uploaded_file_url': uploaded_file_url})

    return JsonResponse({'status': 'error', 'message': 'No file uploaded'})

def list_history_files(request):
    history_files_path = os.path.join(settings.MEDIA_ROOT, 'history')
    files = [
        {
            'name': filename,
            'download_url': settings.MEDIA_URL + 'history/' + filename
        }
        for filename in os.listdir(history_files_path)
        if os.path.isfile(os.path.join(history_files_path, filename))
    ]
    return JsonResponse(files, safe=False)