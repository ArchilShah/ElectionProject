from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('engine.urls')),
    url(r'^engine/', include('engine.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
