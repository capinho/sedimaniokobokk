"""django_shop_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include,re_path,reverse_lazy

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required
from orders.views import *
from django.contrib.auth import update_session_auth_hash


admin.site.site_header = 'Administration Commande Poulets et oeufs SEDIMA '

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^cart/', include(('cart.urls', 'cart'), namespace='cart')),
    re_path(r'^orders/', include(('orders.urls', 'orders'), namespace='orders')),
    re_path(r'^payment/', include(('payment.urls', 'payment'), namespace='payment')),
    #path(r'^paypal/', include('paypal.standard.ipn.urls')),
    re_path(r'^', include(('shop.urls', 'shop'), namespace='shop')),
    re_path(r'^users/login/$', auth.LoginView.as_view(template_name='orders/login.html'), name='login'),
    re_path(r'^users/logout/$',pagelogout,name='logout'),
    #re_path(r'^users/change_password/$', login_required(auth.PasswordChangeView), {'post_change_redirect' : '/','template_name': 'orders/order/change_password.html'}, name='change_password'),
    re_path(r'^users/change_password/$', auth.PasswordChangeView.as_view(template_name= 'orders/order/change_password.html'), name='change_password'),
    re_path(r'^users/change_password/done/$', login_required(auth.PasswordChangeDoneView.as_view(template_name= 'orders/order/password_change_done.html')), name='password_change_done'),

    re_path(r'^', include('templated_email.urls', namespace='templated_email')),

]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL,
#                          document_root=settings.MEDIA_ROOT)
