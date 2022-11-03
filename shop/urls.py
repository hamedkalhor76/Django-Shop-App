# Urls.py in shop app
from . import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:pk>/', views.product, name='product'),
    path('store/', views.store, name='store'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('to-bank/<int:order_id>/', views.to_bank, name='to_bank'),
    path('verify/', views.verify, name='verify'),
    path('callback/', views.callback, name='callback'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
