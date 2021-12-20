from rest_framework import viewsets
from .models import Project, Issues, Milestones, Comments
from .serializer import ProjectSerializer, IssueSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

# Create your views here.


class ProjectView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data.dict()
        if Project.verify_project_name(data['name'], data['admin']):
            return Response({'message': 'You already have a project with this name', 'status': status.HTTP_200_OK})

        data['admin'] = User.objects.get(id=request.user)
        try:
            Project.objects.create(**data)
            return Response({'message': 'Project created successfully', 'status': status.HTTP_200_OK})
        except Exception as error:
            return Response({'error': str(error), 'status': status.HTTP_400_BAD_REQUEST})

    def retrieve(self, request, pk=None):
        project = Project.objects.get(id=pk)
        project_serialized = ProjectSerializer(project)
        return Response(project_serialized.data)

    def list(self, request):
        all_projects = Project.objects.all()
        all_projects_serialized = ProjectSerializer(all_projects, many=True)
        return Response(all_projects_serialized.data)

    def update(self, request, pk=None):
        data = request.data.dict()
        data['admin'] = User.objects.get(id=data['admin'])
        try:
            Project.objects.filter(id=pk).update(**data)
            return Response({'message': 'Project Updated Successfully', 'status': status.HTTP_200_OK})
        except Exception as error:
            return Response({'error': str(error), 'status': status.HTTP_400_BAD_REQUEST})

    def destroy(self, request, pk=None):
        try:
            Project.objects.get(id=pk).delete()
            return Response({'message': 'Project Deleted Successfully', 'status': status.HTTP_200_OK})
        except Exception as error:
            return Response({'error': str(error), 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

    @action(methods='POST', detail=False)
    def add_project_members(self, request):
        user_id = request.data['user_id']
        project_id = request.data['project_id']
        try:
            project = Project.objects.get(id=project_id)
            project.project_members.add(user_id)
            return Response({'message': 'User Added To project', 'status': status.HTTP_200_OK})
        except Exception as error:
            return Response({'error': str(error), 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

    @action(methods='POST', detail=False)
    def remove_members(self, request):
        user_id = request.data['user_id']
        project_id = request.data['project_id']
        try:
            project = Project.objects.get(id=project_id)
            project.project_members.remove(user_id)
            return Response({'message': 'User Removed from project', 'status': status.HTTP_200_OK})
        except Exception as error:
            return Response({'error': str(error), 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})


class IssueView(viewsets.ViewSet):

    def create(self, request):
        data = request.data.dict()
        data['created_by'] = User.objects.get(id=int(data['created_by']))
        try:
            Issues.objects.create(**data)
            return Response({'message': 'Issue Created Successfully', 'status': status.HTTP_200_OK})
        except Exception as error:
            return Response({'error': str(error), 'status': status.HTTP_400_BAD_REQUEST})

    def list(self, request):
        user = User.objects.get(id=request.data['id'])
        all_issues = Issues.objects.filter(created_by=user)
        serialized_issues = IssueSerializer(all_issues, many=True)
        return Response(serialized_issues.data)

    def update(self, request, pk=None):
        data = request.data.dict()
        data['created_by'] = User.objects.get(id=int(data['created_by']))
        try:
            Issues.objects.filter(id=pk).update(**data)
            return Response({'message': 'Issue Updated Successfully', 'status': status.HTTP_200_OK})
        except Exception as error:
            return Response({'error': str(error), 'status': status.HTTP_400_BAD_REQUEST})

    def destroy(self, request, pk=None):
        try:
            Issues.objects.get(id=pk).delete()
            return Response({'message': 'Issue Deleted Successfully', 'status': status.HTTP_200_OK})
        except Exception as error:
            return Response({'error': str(error), 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})
