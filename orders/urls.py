from django.urls import path, re_path,include
from . import task
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.site.site_header = 'Administration Commande Poulets et oeufs SEDIMA '
app_name='orders'
urlpatterns = [
        path('orders/', include('django.contrib.auth.urls')),

        re_path(r'^create/$',
            views.order_create,
            name='order_create'),

        re_path(r'^commande/$', views.list_commande, name='list_commande'),
        re_path(r'^detail_list/(?P<pk>\d+)/$', views.view_list, name='detail_list'),

        path('password_reset/', views.PasswordResetView.as_view(),name='password_reset'),
      
        re_path(r'^password_reset/done/$', views.PasswordResetDoneView.as_view(),name='password_reset_done'),
         
        re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),

        re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
        
        re_path(r'^reset/$',views.reset_template, name='reset_template'),


]
