
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def upvotes(self):
        return self.votes.filter(vote_type='up').count()

    def downvotes(self):
        return self.votes.filter(vote_type='down').count()

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class CommentEvents(models.Model):
    events = models.ForeignKey('Events', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class Vote(models.Model):
    VOTE_TYPE_CHOICES = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=4, choices=VOTE_TYPE_CHOICES)

    class Meta:
        unique_together = ('user', 'post')

class Events(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	text = models.TextField()
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	location = models.CharField(max_length=200)
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	image = models.ImageField(upload_to='event_images/', blank=True, null=True, default='')

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

class VoteEvents(models.Model):
    VOTE_TYPE_CHOICES = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    events = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=4, choices=VOTE_TYPE_CHOICES)

    class Meta:
        unique_together = ('user', 'events')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='default.png')

    def __str__(self):
        return f'{self.user.username} Profil'