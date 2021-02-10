from django.urls import path

import views


urlpatterns = [
    path('ads/', views.AdListView.as_view()),
    path('ads/<int:pk>', views.AdDetailView.as_view())
]