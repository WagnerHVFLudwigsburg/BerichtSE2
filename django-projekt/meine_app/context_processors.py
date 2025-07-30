from .models import Profile

def profilbild_globally(request):
    if request.user.is_authenticated:
        try:
            return {'profilbild': request.user.profile.image.url}
        except Profile.DoesNotExist:
            return {'profilbild': None}
    return {'profilbild': None}