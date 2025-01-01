from __future__ import absolute_import, unicode_literals

# 导入 Celery 应用
from .celery import app as celery_app

__all__ = ('celery_app',)
