import random

from django.db import models

class Story(models.Model):
    body = models.TextField()
    author_name = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "<Story author_name='%s', body='%s...'...>" % (
            self.author_name,
            self.body[0:20],)

    def ordered_images(self):
        """ Images ordered according to order in which they were saved. """
        return self.images.order_by('story_images__id')

class Image(models.Model):
    url = models.CharField(max_length=200)
    typeface = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    author_url = models.CharField(max_length=200)
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    stories = models.ManyToManyField(
        Story, related_name='images', through='StoryImage', null=True)

    @classmethod
    def random(kls, count=1):
        # todo: implement so that it doesn't accidentally
        # use the same image more than once
        #imgs = kls.objects.all()
        #return [random.choice(imgs) for _ in xrange(count)]
        # if we don't care about performance, can use:
        return kls.objects.order_by('?')[:count]

    def __unicode__(self):
        return "<Image url='%s', ...>" % self.url


class StoryImage(models.Model):
    story = models.ForeignKey(Story, related_name='story_images')
    image = models.ForeignKey(Image, related_name='story_images')

    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "<StoryImage %s...<->%s>" % (self.story.body[0:20], self.image.url)

def create_fake_data():
    """ Just some 'fixtures' in case we axe the db. """
    s = Story.objects.create(body="farfrompuken is so awesome, i just love it.",
                             author_name="jared nuzzolillo")

    img_urls = ("http://typequoting.com/images/b-alfred-hitchcock.png",
                "http://typequoting.com/images/d-power-outlet.png",
                "http://typequoting.com/images/f-sink.png",
                "http://typequoting.com/images/k-popeye.png",
                "http://typequoting.com/images/m-mountain.png",
                "http://typequoting.com/images/p-snoopy.png",
                "http://typequoting.com/images/t-tnt.png",)

    for i, img_url in enumerate(img_urls):
        StoryImage.objects.create(
            story=s,
            image=Image.objects.create(
                url=img_url,
                typeface="Typeface %d" % i,
                author_name="Johnny %d Times" % i,
                author_url="http://somewherecool%d" % i,
                body="Cool Story Bro" * i))
