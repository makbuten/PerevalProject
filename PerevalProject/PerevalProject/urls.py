"""
URL configuration for PerevalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pereval.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'submitData', PerevalAddedViewSet)
router.register(r'users', UsersViewSet)
router.register(r'coords', CoordViewSet)
router.register(r'images', ImagesViewSet)
router.register(r'levels', LevelsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/perevaladded/', PerevalAddedListAPIView.as_view()),
    path('api/v1/perevaladdeddetail/<int:pk>', PerevalAddedDetailAPIView.as_view()),
    path('api/v1/users/', UsersListAPIView.as_view()),
    path('api/v1/usersdetail/<int:pk>', UserDetailAPIView.as_view()),
    path('api/v1/images/', ImagesListAPIView.as_view()),
    path('api/v1/imagesdetail/<int:pk>', ImagesDetailAPIView.as_view()),
    path('api/v1/coords/', CoordsListAPIView.as_view()),
    path('api/v1/coordsdetail/<int:pk>', CoordsDetailAPIView.as_view()),
    path('api/v2/', include(router.urls)),

]
