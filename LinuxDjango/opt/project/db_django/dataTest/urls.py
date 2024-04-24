# dataTest/urls.py

from django.urls import path
from .views import dispatcher_databases_view,run_sql_query

urlpatterns = [
    path('import-database/', dispatcher_databases_view, name='dispatcher_databases_view'),
    path('run-query/', run_sql_query, name='run_sql_query'),  
]
