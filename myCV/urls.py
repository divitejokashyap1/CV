from django.urls import path
from .views import resume_images_view
urlpatterns = [
    path('', resume_images_view, name='resume'),
]