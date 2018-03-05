from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('', views.index, name='index'),
        path('ajax/validate_ooxx/', views.validate_ooxx, name='validate_ooxx'),
        path('ajax/add_comment/', views.add_comment, name='add_comment'),
        path('ajax/get_comment/', views.get_comment, name='get_comment'),
        path('ajax/validate_comment_ooxx/', views.validate_comment_ooxx, name='validate_comment_ooxx'),
]
