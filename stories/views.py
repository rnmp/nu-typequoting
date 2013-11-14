from django.shortcuts import render, redirect

from .forms import StoryForm
from .models import Image, Story


def index(request):
    # create a story to hold the images
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_story')
        else:
            image_ids = request.POST.getlist('images', [])
            imgs = [Image.objects.get(pk=image_id) for image_id in image_ids]
    else:
        imgs = Image.random(5)
        form = StoryForm(initial={'images': [img.id for img in imgs]})
    return render(request, 'stories/index.html', {
        'images': imgs,
        'form': form,
    })


def show_story(request):
    stories = Story.objects.order_by('-id').all()
    # process images ahead of time so that they are in the correct order
    return render(request, 'stories/show_story.html', {
        'stories': stories,
    })

def image_gallery(request):
    images = Image.objects.order_by('-id').all()
    return render(request, 'stories/image_gallery.html', {
        'images': images,
    })
