from django.urls import path

from . import views


urlpatterns = [
    path('ads/<uuid:id>/', views.AdDetailView.as_view()),
    path('ads/', views.AdListView.as_view())
]
