# generator/urls.py

from django.urls import path
from . import views
from .views import list_history_files,generate_data,generate_sql

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('upload/', views.file_upload, name='file_upload'),
    # 其他 URL 配置...
    path('history-files/', list_history_files, name='list_history_files'),
    path('generate-data/', generate_data, name='generate_data'),
    path('generate-sql/', generate_sql, name='generate_sql'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
