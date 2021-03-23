from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone

# Create your models here.

# def upload_location(instance, filename):
# 	return "%s/%s" %(instance.id, filename)

class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.DO_NOTHING)
	title = models.CharField(max_length=200)
	content = models.TextField()
	slug = models.SlugField(unique=True)
	image = models.FileField(null=True, blank=True)
	# image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field", height_field="height_field")
	# height_field = models.IntergerField(default=0)
	# width_field = models.IntergerField(default=0)
	draft = models.BooleanField(default=False)
	publish = models.DateTimeField(auto_now=False, auto_now_add=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PostManager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("detail", kwargs={"slug":self.slug})
		#return "/posts/%s" %(self.pk)

	def update_url(self):
		return reverse("update", kwargs={"slug":self.slug})

	def delete_url(self):
		return reverse("delete", kwargs={"slug":self.slug})

	class Meta:
		ordering = ["-timestamp", "-updated"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    if qs.exists():
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)