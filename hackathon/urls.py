from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HackathonViewSet, ProjectViewSet, ApplyToHackathonView

router = DefaultRouter()
router.register(r'hackathons', HackathonViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('apply/', ApplyToHackathonView.as_view(), name='apply-to-hackathon'),
]