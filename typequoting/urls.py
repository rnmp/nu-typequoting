from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'stories.views.index', name='index'),
    url(r'^submissions/$', 'stories.views.submissions', name='submissions'),
    url(r'^submissions/popular$',
        'stories.views.popular_submissions',
        name='popular_submissions'),
    url(r'^about/$', 'stories.views.about_page', name='about_page'),
    url(r'^admin/', include(admin.site.urls)),

    (r'^s/', include('stories.urls', namespace="s")),
)
