from django.shortcuts import render

from rest_framework import viewsets
from .models import Resource
from .serializers import ResourceSerializer

# 下面是展示服务器资源信息导入的包
import psutil
from django.http import JsonResponse
from django.db import connection
from django.apps import apps

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

import subprocess

# Create your views here.
class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

def system_status(request):
    # 获取 CPU 使用率
    cpu_percentage = psutil.cpu_percent(interval=1)

    # 获取内存使用情况
    memory = psutil.virtual_memory()
    memory_total = memory.total
    memory_used = memory.used
    memory_percentage = memory.percent

    # 获取磁盘使用情况
    disk_usage = psutil.disk_usage('/')
    disk_total = disk_usage.total
    disk_used = disk_usage.used
    disk_percentage = disk_usage.percent

    # 获取网络信息
    network = psutil.net_io_counters()
    bytes_sent = network.bytes_sent
    bytes_recv = network.bytes_recv

    # 组装数据
    data = {
        'cpu_percentage': [cpu_percentage] * 5,
        'memory_total': [memory_total] * 5,
        'memory_used': [memory_used] * 5,
        'memory_percentage': [memory_percentage] * 5,
        'disk_total': [disk_total] * 5,
        'disk_used': [disk_used] * 5,
        'disk_percentage': [disk_percentage] * 5,
        'bytes_sent': [bytes_sent] * 5,
        'bytes_recv': [bytes_recv] * 5,
    }

    # 返回 JSON 响应
    return JsonResponse(data)

def database_status(request):
    # 获取数据库详细信息
    # 获取数据库大小
    def get_database_size():
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_schema 'db_name', "
                           "ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) 'db_size_mb' "
                           "FROM information_schema.tables "
                           "WHERE table_schema = DATABASE() GROUP BY table_schema;")
            size = cursor.fetchone()
        return size[1] if size else 'Unknown'

    # 获取表数量
    def get_table_count():
        return len(apps.get_models())

    # 获取每个表的行数和大小
    def get_table_details():
        table_details = {}
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_name, table_rows, "
                           "ROUND((data_length + index_length) / 1024 / 1024, 1) "
                           "FROM information_schema.tables "
                           "WHERE table_schema = DATABASE();")
            rows = cursor.fetchall()
        for row in rows:
            table_name, row_count, size_mb = row
            table_details[table_name] = {'row_count': row_count, 'size_mb': size_mb}
        return table_details

    # 组装数据
    data = {
        'database_size_mb': [get_database_size()]*5,
        'table_count': [get_table_count()]*5,
        'table_details': [get_table_details()]*5,
    }

    # 返回JSON响应
    return JsonResponse(data)

# 假设您使用Celery，需要引入celery的库
from db_django.celery import app

def application_status(request):
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now()).count()
    active_users = User.objects.filter(last_login__gte=timezone.now() - timedelta(minutes=30)).count()
    total_users = User.objects.count()

    # Celery任务状态（需要Celery和其后端存储）
    i = app.control.inspect()
    active_tasks = len(i.active() if i.active() else [])
    scheduled_tasks = len(i.scheduled() if i.scheduled() else [])
    reserved_tasks = len(i.reserved() if i.reserved() else [])
    # failed_tasks = len(i.failed() if i.failed() else [])  # 需要Celery的Failure backend
    
    data = {
        'active_sessions': [active_sessions]*5,
        'active_users': [active_users]*5,
        'total_users': [total_users]*5,
        'active_celery_tasks': [active_tasks]*5,
        'scheduled_celery_tasks': [scheduled_tasks]*5,
        'reserved_celery_tasks': [reserved_tasks]*5,
        # 'failed_celery_tasks': failed_tasks,
    }

    return JsonResponse(data)

def network_status(request):
    def get_ping_latency(host='baidu.com'):
        process = subprocess.Popen(['ping', '-c', '4', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = process.communicate()
        if process.returncode == 0:
            result_lines = out.decode('utf-8').splitlines()
            ping_stats = result_lines[-1].split('/')
            latency = float(ping_stats[-3])
            return latency
        return 'Error'

    network_stats = psutil.net_io_counters(pernic=False)
    packets_sent = network_stats.packets_sent
    packets_recv = network_stats.packets_recv
    errin = network_stats.errin
    errout = network_stats.errout
    dropin = network_stats.dropin
    dropout = network_stats.dropout
    
    data = {
        # 'ping_latency': get_ping_latency(),
        'packets_sent': [packets_sent]*5,
        'packets_recv': [packets_recv]*5,
        'errin': [errin]*5,
        'errout': [errout]*5,
        'dropin': [dropin]*5,
        'dropout': [dropout]*5,
    }

    return JsonResponse(data)