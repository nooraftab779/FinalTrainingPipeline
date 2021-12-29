from django.urls import path
from . import views

urlpatterns = [
    path('monitor/', views.monitor, name='monitor'),
    # path('graph/',views.graph , name='graph')
]
