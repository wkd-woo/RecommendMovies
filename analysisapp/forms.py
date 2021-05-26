from django.forms import ModelForm

from analysisapp.models import Rating, Results

class ResultsCreationForm(ModelForm):
    class Meta:
        model = Results
        fields = '__all__'



class RatingCreationForm(ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'