from urllib.parse import quote_plus
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.timezone import datetime
from django.db.models import Q

from .models import Post
from .forms import PostForm

# Create your views here.
def post_list(request): # list_details
	today = timezone.now()
	queryset= Post.objects.active()#.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset = Post.objects.all()
	query = request.GET.get('q')
	if query:
		queryset = queryset.filter(
			Q(content__icontains=query)|
			Q(title__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()
	paginator = Paginator(queryset, 2)
	page = request.GET.get('page')
	page_obj = paginator.get_page(page)

	context = {
		'query' : query,
		'today' : today,
		'page_obj': page_obj,
	}
	return render(request, 'post_list.html', context)
    
def post_add(request): # Create_a_post
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save()
		instance.user = request.user
		messages.success(request, "Post Created!")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"Title" : "Create Post",
		"form" : form,
	}
	return render(request, 'post_create.html', context)

def post_detail(request, slug=None): # retrive_data
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	context = {
		'instance' : instance,
		'share_string' : share_string,
	}
	return render(request, 'post_detail.html', context)


def post_update(request, slug=None): # Make_changes
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance= get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		form.save()
		messages.success(request, "Post Updated!")
		return HttpResponseRedirect(instance.get_absolute_url()) 

	context = {
		"form" : form,
		"instance" : instance,
		"Title" : "Edit Post",
	}
	return render(request, 'post_create.html', context)

def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Post Deleted!")
	return redirect("post")