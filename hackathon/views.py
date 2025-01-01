from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Hackathon, Project, ProjectHackathon
from .serializers import HackathonSerializer, ProjectSerializer
from django.utils.timezone import now
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer
from .tasks import send_email_task

class HackathonViewSet(viewsets.ModelViewSet):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]  # 只有 is_staff 用户可以创建
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # 允许任何人查看 hackathon 列表和详情
        return [IsAuthenticated()]  # 其他操作需要登录用户

    def perform_create(self, serializer):
        # 自动将当前用户设置为 hackathon 的创建者
        serializer.save(created_by=self.request.user)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 返回当前用户创建的项目
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 创建时自动将 user 设置为当前登录用户
        serializer.save(user=self.request.user)

        project = serializer.save(user=self.request.user)
        # 调用异步任务
        send_email_task.delay(self.request.user.email, project.title)


class ApplyToHackathonView(APIView):
    def post(self, request, *args, **kwargs):
        project_id = request.data.get('project_id')
        hackathon_id = request.data.get('hackathon_id')

        # 验证 Project 是否属于当前用户
        project = get_object_or_404(Project, id=project_id, user=request.user)
        hackathon = get_object_or_404(Hackathon, id=hackathon_id)

        try:
            # 创建中间表记录，并设置 apply_time
            ProjectHackathon.objects.create(
                project=project,
                hackathon=hackathon,
                apply_time=now()
            )
        except IntegrityError:
            raise ValidationError(f"Project '{project.title}' has already applied to Hackathon '{hackathon.title}'.")

        return Response(
            {'message': f"Project '{project.title}' successfully applied to Hackathon '{hackathon.title}'!"},
            status=status.HTTP_200_OK
        )