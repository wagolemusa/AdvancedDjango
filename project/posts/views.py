# from urllib import quote_plus
from urllib.parse import quote_plus  
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import Q

# Create your views here.
from .models import Post
from .forms import PostForms

def post_create(request):
	"""
	Methods creates the Posts
	"""
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
		
	form = PostForms(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_obsolute_url())
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)


def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
	}
	return render(request, "post_detail.html", context)


def post_list(request):
	""" list items """
	today = timezone.now().date()
	querySet_list = Post.objects.all()

	if request.user.is_staff or request.user.is_superuser:
		querySet_list = Post.objects.all()

	# Search posts
	query = request.GET.get("q")
	if query:
		querySet_list = querySet_list.filter(
							Q(title__icontains=query)|
							Q(content__icontains=query)|
							Q(user__username__icontains=query)
							).distinct()

	paginator = Paginator(querySet_list, 3)
	page = request.GET.get('page')
	querySet = paginator.get_page(page)

	context = {
		"query_list": querySet,
		"title":"list",
		"today": today
	}
	return render(request, "post_list.html", context)
	

def post_update(request, slug=None):
	"""
	It updates posts
	"""
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForms(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# message success
		messages.success(request, "Successfuly updated")
		return HttpResponseRedirect(instance.get_obsolute_url())
	else:
		messages.error(request, "Not update")
	context = {
	"title": instance.title,
	"instance": instance,
	"form": form,
	}
	return render(request, "post_form.html", context)


def post_delete(request, slug=None):
	"""
	 delete Details 
	"""
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfuly Deleted")
	return redirect("posts:list")

