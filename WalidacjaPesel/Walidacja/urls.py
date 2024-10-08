from django.urls import path

from .views import PeselValidation, ResultView

urlpatterns = [
    path('', PeselValidation.as_view(), name='home'),
    path('result/', ResultView.as_view(), name='result')
]
