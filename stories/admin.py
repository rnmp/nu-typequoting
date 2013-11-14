from django.contrib import admin
from stories.models import Image, Story, StoryImage

admin.site.register(Image)
admin.site.register(Story)
admin.site.register(StoryImage)