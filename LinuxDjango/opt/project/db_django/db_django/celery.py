# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置 Django 的默认设置模块。
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db_django.settings')

app = Celery('db_django')

# 使用 Django 的设置文件来配置 Celery。
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从所有已注册的 Django app 中加载任务。
app.autodiscover_tasks()

# 如果您使用 Redis 作为消息代理，配置如下：
app.conf.broker_url = 'redis://localhost:6379/0'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
