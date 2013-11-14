from django.forms import ModelForm, ModelMultipleChoiceField, MultipleHiddenInput

from .models import Image, Story, StoryImage

class StoryForm(ModelForm):
    images = ModelMultipleChoiceField(
        queryset=Image.objects.all(),
        widget=MultipleHiddenInput
    )

    class Meta:
        model = Story

    def clean__author_name(self):
        return self.cleaned_data.get('author_name', 'Anonymous')
    
    def clean_images(self):
        """ We need to order the fancy ModelMultipleChoiceField via basic data. """
        image_ids = [int(image_id) for image_id in self.data.getlist('images')]
        return sorted(
            self.cleaned_data['images'], 
            key=lambda img: image_ids.index(img.pk))
        # sort the items in images according to the index of the place it appears in image_id

    def save(self, *args, **kwargs):
        super(StoryForm, self).save(*args, **kwargs)
        for img in self.cleaned_data.get('images'):
            StoryImage.objects.create(story=self.instance, image=img)
        return self.instance 
