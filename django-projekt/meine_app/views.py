from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Post, Vote, Events, VoteEvents, Profile
from .forms import PostForm, CommentForm, EventsForm, ProfileForm, CommentEvents

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def events(request):
	events = Events.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	
	events_with_votes = []
	for event in events:
		upvotes = event.votes.filter(vote_type='up').count()
		downvotes = event.votes.filter(vote_type='down').count()
		events_with_votes.append({
			'event': event,
			'upvotes': upvotes,
			'downvotes': downvotes
		})
	
	return render(request, "events.html", {'events_with_votes': events_with_votes})

def events_detail(request, pk):
    events = get_object_or_404(Events, pk=pk)
    upvotes = events.votes.filter(vote_type='up').count()
    downvotes = events.votes.filter(vote_type='down').count()
    return render(request, 'events_detail.html', {
        'events': events,
        'upvotes': upvotes,
        'downvotes': downvotes
    })

@login_required
def events_new(request):
    if request.method == "POST":
        form = EventsForm(request.POST, request.FILES)
        if form.is_valid():
            events = form.save(commit=False)
            events.author = request.user
            events.published_date = timezone.now()
            events.save()
            return redirect('events_detail', pk=events.pk)
    else:
        form = EventsForm()
    return render(request, 'events_edit.html', {'form': form})

@login_required
def events_edit(request, pk):
	events = get_object_or_404(Events, pk=pk)
	if request.method == "POST":
		form = EventsForm(request.POST, request.FILES, instance=events)
		if form.is_valid():
			events = form.save(commit=False)
			events.author = request.user
			events.published_date = timezone.now()
			events.save()
			return redirect('events_detail', pk=events.pk)
	else:
		form = EventsForm(instance=events)
	return render(request, 'events_edit.html', {'form': form})

@login_required
def add_comment_to_events(request, pk):
    events = get_object_or_404(Events, pk=pk)
    if request.method == "POST":
        form = CommentEvents(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.events = events
            comment.save()
            return redirect('events_detail', pk=events.pk)
    else:
        form = CommentEvents()
    return render(request, 'add_comment_to_events.html', {'form': form})



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    posts_with_votes = []
    for post in posts:
        upvotes = post.votes.filter(vote_type='up').count()
        downvotes = post.votes.filter(vote_type='down').count()
        posts_with_votes.append({
            'post': post,
            'upvotes': upvotes,
            'downvotes': downvotes
        })

    return render(request, 'post.html', {'posts_with_votes': posts_with_votes})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    upvotes = post.votes.filter(vote_type='up').count()
    downvotes = post.votes.filter(vote_type='down').count()
    return render(request, 'post_detail.html', {
        'post': post,
        'upvotes': upvotes,
        'downvotes': downvotes
    })

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})

@login_required
def vote_up(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Vote.objects.update_or_create(user=request.user, post=post, defaults={'vote_type': 'up'})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def events_vote_up(request, pk):
    events = get_object_or_404(Events, pk=pk)
    VoteEvents.objects.update_or_create(user=request.user, events=events, defaults={'vote_type': 'up'})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def events_vote_down(request, pk):
    events = get_object_or_404(Events, pk=pk)
    VoteEvents.objects.update_or_create(user=request.user, events=events, defaults={'vote_type': 'down'})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def vote_down(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Vote.objects.update_or_create(user=request.user, post=post, defaults={'vote_type': 'down'})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def meine_likes(request):
    liked_votes = Vote.objects.filter(user=request.user, vote_type='up').select_related('post')
    posts = [vote.post for vote in liked_votes]
    return render(request, 'meine_likes.html', {'posts': posts})

@login_required
def meine_events(request):
    liked_votes = VoteEvents.objects.filter(user=request.user, vote_type='up').select_related('events')
    events = [vote.events for vote in liked_votes]
    return render(request, 'meine_events.html', {'events': events})

@login_required
def profil_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profil.html', {'form': form, 'profile': profile})

def report_jpg(request):
    return render(request, "report_jpg.html")

