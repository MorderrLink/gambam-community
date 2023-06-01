"""
URL configuration for gambam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

# all views import
from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('home/', views.home, name="home"),
    path('', views.home_redir, name="home-redir"),
    path('about/', views.about, name="about"),
    path('blog/', views.blog, name = "blog"),
    path('profile/', views.profile, name = "profile"),
    path('galery', views.galery, name="galery"),
        path('favicon.ico/',RedirectView.as_view(url='\\static\\image\\favicon.ico')),
    # autentification
    path('accounts/', include('allauth.urls')),  
    path('accounts/profile/', views.callback, name="callback-redirect"),
    path('accounts/logout/', views.account_logout_redir, name="account_logout_redir"),

    # cart + shop
    path('update_item/', views.updateItem, name="update-item"),
    path('shop/', views.shop, name = "shop"),
    path('product/id=<int:product_id>&<slug:slug>', views.product, name="product"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('sucsess/', views.success, name="success"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)