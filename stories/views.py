from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect

from .forms import StoryForm
from .models import Image, Story
from typequoting.utils import JsonResponse


def index(request):
    # create a story to hold the images
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You just created this!')
            return redirect('recent_submissions')
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


def _submissions(request, qs, page_type):
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', 1)
    try:
        stories_page = paginator.page(page)
    except PageNotAnInteger:
        stories_page = paginator.page(1)
    except EmptyPage:
        stories_page = paginator.page(paginator.num_pages)
    return render(request, 'stories/submissions.html', {
        'stories_page': stories_page,
        'pages': paginator.page_range,
        'page_type': page_type,
    })

def popular_submissions(request):
    return _submissions(
        request, Story.objects.filter(
            like_count__gt=0).order_by('-like_count'), "popular")

def recent_submissions(request):
    return _submissions(
        request, Story.objects.order_by('-id'), "recent")

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


def like(request, story_id):
    try:
        story = get_object_or_404(Story, pk=story_id)
    except Story.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cannot be found.'})
    #if request.COOKIES.has_key('already_voted_on_%s' % story_id):
    #    return JsonResponse({'success': False, 'message': 'Already voted.'})
    #else:
    story.like()
    story.save()
    resp = JsonResponse({'success': True, 'like_count': story.like_count})
    resp.set_cookie('already_voted_on_%d' % story.id)
    return resp
