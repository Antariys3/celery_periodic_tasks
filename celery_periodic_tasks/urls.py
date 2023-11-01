"""
URL configuration for celery_periodic_tasks project.

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
from django.urls import path

from exchange.views import exchange_rates, home, exchange_calculator

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('exchange_rates/', exchange_rates, name="exchange_rates"),
    path('exchange_calculator/', exchange_calculator, name="exchange_calculator"),
]
