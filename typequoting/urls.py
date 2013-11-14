from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'stories.views.index', name='index'),
    url(r'^submissions$', 'stories.views.show_story', name='show_story'),
    url(r'^images$', 'stories.views.image_gallery', name='image_gallery'),

    url(r'^admin/', include(admin.site.urls)),
)
