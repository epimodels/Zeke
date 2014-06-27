from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin


# http://stackoverflow.com/questions/3718077/
#\django-you-dont-have-permission-to-edit-anything
admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^$', 'zeke.views.root'),
                       url(r'^about/', 'zeke.views.about'),
                       url(r'^contact/', 'zeke.views.contact'),
                       url(r'^login/', 'zeke.views._login'),
                       url(r'^logout/', 'zeke.views._logout'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^plot$', 'zeke.views.plot'),)
