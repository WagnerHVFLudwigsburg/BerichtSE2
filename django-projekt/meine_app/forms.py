from django import forms

from .models import Post, Comment, Events, Profile, CommentEvents

class PostForm(forms.ModelForm):

    class Meta:
         model = Post
         fields = ('title', 'text', 'image')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class CommentEvents(forms.ModelForm):

    class Meta:
        model = CommentEvents
        fields = ('author', 'text',)


class EventsForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d', '%d.%m.%Y'], 
        label='Startdatum'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d', '%d.%m.%Y'],
        label='Enddatum'
    )

    class Meta:
        model = Events
        fields = ['title', 'location', 'start_date', 'end_date', 'text', 'image']
 
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']