"""FastCan URL Configuration

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

from django.conf.urls import url
from django.contrib import admin
from GroupMatchingModel import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.Login),
    url(r'^logout/$', views.Logout),
    url(r'^signup/$', views.SignUp),
    url(r'^home/$', views.ShowMessage),
    url(r'^project/create/$', views.createProject),
    url(r'^group/create/$', views.createGroup),
    url(r'^group/join/$', views.joinGroup),
    url(r'^ajax/load-group/$', views.loadGroup, name='ajax_load_group'),
    url(r'^group/quit/$', views.quitGroup),
    url(r'^group/show/$', views.ShowGroup),
    url(r'^project/deliver/$', views.DeliverEmail),
    url(r'^project/clear/$', views.ClearProject),
    # url(r'^group/show/$', views.ShowGroup),

]
