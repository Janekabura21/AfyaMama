from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.maternal_profile, name='maternal_profile'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('notifications/', views.notifications, name='notifications'),
]
