from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

from .forms import StoryForm
from .models import Image, Story


def index(request):
    # create a story to hold the images
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You just created this!')
            return redirect('submissions')
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


def submissions(request):
    paginator = Paginator(Story.objects.order_by('-id'), 20)
    page = request.GET.get('page')
    try:
        stories_page = paginator.page(page)
    except PageNotAnInteger:
        stories_page = paginator.page(1)
    except EmptyPage:
        stories_page = paginator.page(paginator.num_pages)
    # process images ahead of time so that they are in the correct order
    return render(request, 'stories/submissions.html', {
        'stories_page': stories_page,
        'pages': paginator.page_range,
    })

def view_story(request, story_id):
    story = Story.objects.get(id=story_id) 
    return render(request, 'stories/view_story.html', {
        'story': story,
    })

def about_page(request):
    images = Image.objects.order_by('name').all()
    return render(request, 'about.html', {
        'images': images,
    })
