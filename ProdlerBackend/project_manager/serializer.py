from rest_framework import serializers
from .models import Project, Milestones, Issues, Comments
from user_manager.serializer import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    project_members = UserSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'admin', 'name', 'project_members', 'created_on', 'tags']


class IssueSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Issues
        fields = ['id', 'created_by', 'title', 'details', 'created_on', 'tags']
