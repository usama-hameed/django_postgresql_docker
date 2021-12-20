from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('/project', views.ProjectView, basename='Project'),
router.register('/issue', views.IssueView, basename='issue')

urlpatterns = [
    path('', include(router.urls)),
    path('/add_members/', views.ProjectView.as_view({'post': 'add_project_members'}), name='add_project_members'),
    path('/remove_member/', views.ProjectView.as_view({'post': 'remove_members'}), name='remove_members'),
]
