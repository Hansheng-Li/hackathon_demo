from django.contrib import admin
from .models import Hackathon, Project, ProjectHackathon

@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'created_by')
    list_filter = ('start_time', 'end_time')

class ProjectHackathonInline(admin.TabularInline):
    model = Project.hackathons.through  # 引用自定义中间表
    extra = 1  # 默认显示的空行数量

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'get_hackathons')  # 使用自定义方法显示 hackathons
    list_filter = ('user',)
    inlines = [ProjectHackathonInline]  # 添加 Inline

    def get_hackathons(self, obj):
        # 返回与项目关联的所有 hackathons 的标题
        return ", ".join([hackathon.title for hackathon in obj.hackathons.all()])
    get_hackathons.short_description = 'Hackathons'  # 在 Admin 界面中显示的标题

@admin.register(ProjectHackathon)
class ProjectHackathonAdmin(admin.ModelAdmin):
    list_display = ('project', 'hackathon', 'apply_time')
    list_filter = ('apply_time',)
