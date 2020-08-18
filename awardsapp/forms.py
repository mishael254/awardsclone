from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Projects, Rates, Comments

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProjectUploadForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ('title','image_posted','description', 'link')
        
class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')
     
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_photo','bio','website','phone_number') 
        
class VotesForm(forms.ModelForm):
    '''
    Form for rating projects posted
    '''
    class Meta:
        model = Rates
        fields = ('design','usability','content')
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comments',)

        