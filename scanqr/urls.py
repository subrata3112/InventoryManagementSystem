from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('scan', views.scanqr, name='scanqr'),
    path('add', views.add_item, name='add_item'),
    # path('upload_and_scan',views.upload_and_scan, name='upload_and_scan')
]