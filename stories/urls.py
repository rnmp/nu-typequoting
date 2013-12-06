from django.conf.urls import patterns, url


urlpatterns = patterns('stories.views',
    url(r'^(?P<story_id>\d+)$', "view_story", name="view_story"),
    url(r'^(?P<story_id>\d+)/like$', "like", name="like_story"),
)
