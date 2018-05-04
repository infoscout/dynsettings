from django.conf.urls import url
from django.contrib import admin

# set url reference for testing
urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
