import time
from datetime import date
from .models import Project
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(user_email, project_title):
    # 模拟邮件发送
    time.sleep(2)  # 模拟发送延迟
    print(f"Email sent to {user_email} for project {project_title}")

@shared_task
def daily_project_count():
    today = date.today()
    count = Project.objects.filter(created_at__date=today).count()  
    print(f"Projects created today: {count}")
