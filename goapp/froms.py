from django import forms
from analysisapp.models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ('rating_id', 'user_id', 'movie_id', 'timestamp')