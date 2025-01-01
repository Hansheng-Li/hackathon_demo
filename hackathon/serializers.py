from rest_framework import serializers
from .models import Hackathon, Project

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = ['id', 'title', 'start_time', 'end_time', 'created_by']
        read_only_fields = ['created_by']

class ProjectSerializer(serializers.ModelSerializer):
    hackathons = serializers.SerializerMethodField()  # 自定义字段

    class Meta:
        model = Project
        fields = ['id', 'title', 'user', 'hackathons']
        read_only_fields = ['user']

    def get_hackathons(self, obj):
        # 返回与项目关联的 Hackathon 的基本信息
        return [
            {
                "id": hackathon.id,
                "title": hackathon.title
            }
            for hackathon in obj.hackathons.all()
        ]

class ApplyHackathonSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    hackathon_id = serializers.IntegerField()