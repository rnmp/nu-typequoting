from django.db import models


class Story(models.Model):
    body = models.TextField()
    author_name = models.CharField(max_length=200, blank=True)
    like_count = models.IntegerField(default=0, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "<Story author_name='%s', body='%s...'...>" % (
            self.author_name,
            self.body[0:20],)

    def ordered_images(self):
        """ Images ordered according to order in which they were saved. """
        return self.images.order_by('story_images__id')

    def like(self):
        """ Increment the like_count for this story. """
        self.like_count = self.like_count + 1 if self.like_count else 1

    @property
    def has_likes(self):
        return self.like_count and self.like_count > 0

class Image(models.Model):
    url = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    uppercase = models.BooleanField()
    typeface = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    author_url = models.CharField(max_length=200)

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
        return self.name


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

    img_urls = ("https://dl.dropboxusercontent.com/u/190173/typequoting/images/u-B.png",
                "https://dl.dropboxusercontent.com/u/190173/typequoting/images/u-D.png",
                "https://dl.dropboxusercontent.com/u/190173/typequoting/images/l-f.png",
                "https://dl.dropboxusercontent.com/u/190173/typequoting/images/u-K.png",
                "https://dl.dropboxusercontent.com/u/190173/typequoting/images/l-m.png",
                "https://dl.dropboxusercontent.com/u/190173/typequoting/images/u-P.png",
                "https://dl.dropboxusercontent.com/u/190173/typequoting/images/u-T.png",)

    for i, img_url in enumerate(img_urls):
        StoryImage.objects.create(
            story=s,
            image=Image.objects.create(
                url=img_url,
                name="name %d" % i,
                author_name="Johnny %d Times" % i,
                author_url="http://somewherecool%d" % i,
                uppercase="uppercase %d" % i,
                typeface="typeface %d" % i))
