from django.urls import path
from .views import UploadFileView, ResultView

urlpatterns = [
    path('', UploadFileView.as_view(), name='home'),
    path('result/',ResultView.as_view(),name='result')
]
