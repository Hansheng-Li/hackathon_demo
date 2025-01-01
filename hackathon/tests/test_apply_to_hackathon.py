from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from hackathon.models import Project, Hackathon, ProjectHackathon

class ApplyToHackathonAPITest(TestCase):
    def setUp(self):
        # 创建用户
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()

        # 用户登录
        self.client.login(username="testuser", password="password123")

        # 创建 Hackathon 和 Project
        self.hackathon = Hackathon.objects.create(
            title="Test Hackathon",
            start_time="2025-01-01T09:00:00Z",
            end_time="2025-01-02T18:00:00Z",
            created_by=self.user,
        )
        self.project = Project.objects.create(
            title="Test Project",
            user=self.user,
        )

    def test_apply_to_hackathon_success(self):
        """测试项目成功申请加入 Hackathon"""
        url = reverse("apply-to-hackathon")
        data = {
            "project_id": self.project.id,
            "hackathon_id": self.hackathon.id,
        }

        response = self.client.post(url, data, format="json")

        # 检查响应
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("successfully applied", response.data["message"])

        # 验证中间表记录
        exists = ProjectHackathon.objects.filter(
            project=self.project,
            hackathon=self.hackathon,
        ).exists()
        self.assertTrue(exists)

    def test_apply_to_hackathon_project_not_owned(self):
        """测试项目不属于当前用户时，返回 404"""
        other_user = User.objects.create_user(username="otheruser", password="password123")
        other_project = Project.objects.create(
            title="Other User Project",
            user=other_user,
        )
        url = reverse("apply-to-hackathon")
        data = {
            "project_id": other_project.id,
            "hackathon_id": self.hackathon.id,
        }

        response = self.client.post(url, data, format="json")

        # 检查响应
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_apply_to_hackathon_invalid_hackathon(self):
        """测试 Hackathon ID 无效时返回 404"""
        url = reverse("apply-to-hackathon")
        data = {
            "project_id": self.project.id,
            "hackathon_id": 999,  # 不存在的 Hackathon ID
        }

        response = self.client.post(url, data, format="json")

        # 检查响应
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_apply_to_hackathon_missing_fields(self):
        """测试缺少字段时返回 400"""
        url = reverse("apply-to-hackathon")
        data = {
            "project_id": self.project.id,
        }  # 缺少 hackathon_id

        response = self.client.post(url, data, format="json")

        # 检查响应
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
