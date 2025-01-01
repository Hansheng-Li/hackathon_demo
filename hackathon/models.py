from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

class Hackathon(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}
    )

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    hackathons = models.ManyToManyField(
        Hackathon,
        through='ProjectHackathon',
        related_name='projects',
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)  # 添加自动记录创建时间

    def __str__(self):
        return self.title

# 自定义中间表
class ProjectHackathon(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    apply_time = models.DateTimeField(default=timezone.now)  # 默认值为存量数据的时间
    
    class Meta:
        unique_together = ('project', 'hackathon')  # 添加唯一约束
        
    def __str__(self):
        return f"{self.project.title} -> {self.hackathon.title} @ {self.apply_time}"
