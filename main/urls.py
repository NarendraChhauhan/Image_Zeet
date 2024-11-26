from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('upload/', views.upload_image, name='upload_image'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
]
