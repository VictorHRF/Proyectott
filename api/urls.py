from django.urls import path
from .views import EcuacionList, EcuacionDetail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('ec/', EcuacionList.as_view()),
    path('ec/<int:pk>/', EcuacionDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)