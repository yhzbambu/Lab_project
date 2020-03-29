from django.urls import path
from . import views

urlpatterns=[
    path('',views.video_list,name='video_list'),
    path('<str:video_id>',views.video_detail,name='video_detail'),
    path('type/<int:video_type_pk>', views.videos_with_type, name="videos_with_type"),
]

