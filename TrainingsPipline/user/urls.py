from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('available-server/server-reservation/', views.reservation, name='reservation'),
    path('available-server/book-now/', views.book_now, name='book-now'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('available-server/', views.available_server, name='available-server'),
    path('booked-server/', views.booked_server, name='booked-server'),
]
