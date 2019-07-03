from django.urls import path

from pdf.views import MessageView

app_name = 'pdf'
urlpatterns = [
    path('', MessageView.as_view(), name='message')
]