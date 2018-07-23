from django.urls import path
from django.conf.urls import url
from django.urls import include
from myapp import views
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm


app_name = 'myapp'

urlpatterns = [
path(r'', views.index, name='index'),
path(r'about/' , views.about, name='about'),
path(r'detail/<int:cat_no>/', views.detail,name='detail'),
path(r'products/', views.products, name='products'),
path(r'place_order/', views.place_order, name='place_order'),
path(r'products/<int:prod_id>/', views.productdetail, name='product detail'),
path(r'login/', views.user_login, name='login'),
path(r'logout/', views.user_logout, name='logout'),
path(r'myorders/', views.myorders, name='myorders'),
path(r'register/', views.register, name='register'),
path(r'reset-password/', password_reset, name='reset_password'),
path(r'reset-password/done/', password_reset_done, name='password_reset_done'),
path(r'reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', password_reset_confirm, name='password_reset_confirm'),

]
